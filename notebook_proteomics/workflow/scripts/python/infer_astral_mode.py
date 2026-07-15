import argparse
import re
import xml.etree.ElementTree as ET
from pathlib import Path
from zipfile import ZipFile

NS = "{http://schemas.openxmlformats.org/spreadsheetml/2006/main}"


def read_cell_value(cell):
    cell_type = cell.attrib.get("t")
    if cell_type == "inlineStr":
        inline = cell.find(NS + "is")
        if inline is None:
            return ""
        return "".join((node.text or "") for node in inline.iter(NS + "t"))
    value = cell.find(NS + "v")
    return "" if value is None else (value.text or "")


def summarize_xlsx_visible_master_rows(path):
    with ZipFile(path) as archive:
        with archive.open("xl/worksheets/sheet1.xml") as handle:
            context = ET.iterparse(handle, events=("end",))
            header = None
            abundance_start = None
            abundance_end = None
            accession_idx = None
            visible_master_rows = 0
            hidden_rows = 0
            prtc_rows = 0
            prtc_complete = 0
            all_zero = 0
            mixed_rows = 0
            sparse_rows = 0
            complete_rows = 0
            sparse_examples = []

            for _, elem in context:
                if elem.tag != NS + "row":
                    continue

                if elem.attrib.get("hidden") == "1":
                    hidden_rows += 1
                    elem.clear()
                    continue

                values = [read_cell_value(cell) for cell in elem.findall(NS + "c")]
                if header is None:
                    header = values
                    abundance_start = next(
                        i for i, val in enumerate(header)
                        if isinstance(val, str) and val.startswith("Abundances (Grouped):")
                    )
                    abundance_count = sum(
                        1 for val in header
                        if isinstance(val, str) and val.startswith("Abundances (Grouped):")
                    )
                    abundance_end = abundance_start + abundance_count
                    accession_idx = header.index("Accession")
                    elem.clear()
                    continue

                if len(values) < abundance_end:
                    elem.clear()
                    continue

                accession = str(values[accession_idx])
                abundances = []
                for raw in values[abundance_start:abundance_end]:
                    try:
                        abundances.append(float(raw) if raw != "" else 0.0)
                    except ValueError:
                        abundances.append(0.0)

                nonzero = sum(1 for value in abundances if value != 0)
                zero = len(abundances) - nonzero

                visible_master_rows += 1
                if accession.startswith("PRTC-"):
                    prtc_rows += 1
                    if zero == 0:
                        prtc_complete += 1
                if nonzero == 0:
                    all_zero += 1
                elif zero > 0:
                    mixed_rows += 1
                    if 3 <= nonzero <= max(3, len(abundances) - 3):
                        sparse_rows += 1
                        if len(sparse_examples) < 8:
                            sparse_examples.append(
                                {
                                    "accession": accession,
                                    "nonzero": nonzero,
                                    "zero": zero,
                                }
                            )
                else:
                    complete_rows += 1

                elem.clear()

    return {
        "abundance_columns": abundance_end - abundance_start,
        "visible_master_rows": visible_master_rows,
        "hidden_rows": hidden_rows,
        "prtc_rows": prtc_rows,
        "prtc_complete": prtc_complete,
        "all_zero": all_zero,
        "mixed_rows": mixed_rows,
        "sparse_rows": sparse_rows,
        "complete_rows": complete_rows,
        "sparse_examples": sparse_examples,
    }


def build_recommendation(summary):
    total = max(summary["visible_master_rows"], 1)
    mixed_fraction = summary["mixed_rows"] / total
    sparse_fraction = summary["sparse_rows"] / total
    prtc_complete_fraction = (
        summary["prtc_complete"] / summary["prtc_rows"]
        if summary["prtc_rows"] else 0.0
    )

    if mixed_fraction >= 0.25 and sparse_fraction >= 0.10:
        value = True
        explanation = (
            "Many visible proteins have a mix of zero and non-zero abundances across samples, "
            "which is more consistent with zeros acting as missing-value placeholders than with "
            "strict present/absent filtering."
        )
    else:
        value = False
        explanation = (
            "The visible protein matrix is mostly complete or only lightly sparse, so keeping the "
            "legacy non-zero comparison filters is the safer default."
        )

    return {
        "value": value,
        "mixed_fraction": mixed_fraction,
        "sparse_fraction": sparse_fraction,
        "prtc_complete_fraction": prtc_complete_fraction,
        "explanation": explanation,
    }


def load_raw_data_path(manifest_path):
    project_root = manifest_path.parents[3]
    raw_data_file = ""
    with open(manifest_path, "r", encoding="utf-8") as handle:
        for line in handle:
            match = re.match(r"\s*raw_data_file:\s*(.+?)\s*(?:#.*)?$", line)
            if not match:
                continue
            raw_data_file = match.group(1).strip().strip("'\"")
            break
    if not raw_data_file:
        raise KeyError("raw_data_file is missing from project_manifest.yaml")
    return project_root / raw_data_file


def main():
    parser = argparse.ArgumentParser(
        description="Inspect a proteomics workbook and propose a value for analysis.astral_mode."
    )
    parser.add_argument(
        "--manifest",
        default="workflow/00_raw_data/config/project_manifest.yaml",
        help="Path to project_manifest.yaml",
    )
    parser.add_argument(
        "--input",
        default="",
        help="Optional direct path to the raw data workbook; overrides --manifest",
    )
    args = parser.parse_args()

    if args.input:
        input_path = Path(args.input).resolve()
    else:
        input_path = load_raw_data_path(Path(args.manifest).resolve())

    if input_path.suffix.lower() != ".xlsx":
        raise SystemExit(
            "This helper currently supports .xlsx provider workbooks only."
        )

    summary = summarize_xlsx_visible_master_rows(input_path)
    recommendation = build_recommendation(summary)

    print(f"Input workbook: {input_path}")
    print(f"Visible master-protein rows inspected: {summary['visible_master_rows']}")
    print(f"Hidden child/detail rows skipped: {summary['hidden_rows']}")
    print(f"Grouped abundance columns: {summary['abundance_columns']}")
    print(f"PRTC rows detected: {summary['prtc_rows']}")
    print(f"Mixed zero/non-zero rows: {summary['mixed_rows']} ({recommendation['mixed_fraction']:.1%})")
    print(f"Sparser mixed rows (3 to n-3 non-zero samples): {summary['sparse_rows']} ({recommendation['sparse_fraction']:.1%})")
    print(f"All-nonzero rows: {summary['complete_rows']}")
    print(f"All-zero visible rows: {summary['all_zero']}")
    if summary["prtc_rows"]:
        print(f"PRTC rows complete across samples: {summary['prtc_complete']} ({recommendation['prtc_complete_fraction']:.1%})")

    print()
    print(f"Recommended astral_mode: {'true' if recommendation['value'] else 'false'}")
    print(recommendation["explanation"])

    if summary["sparse_examples"]:
        print()
        print("Example mixed rows:")
        for row in summary["sparse_examples"]:
            print(
                f"- {row['accession']}: {row['nonzero']} non-zero, {row['zero']} zero"
            )

    print()
    print(
        "Use this as a project-specific recommendation, not an absolute rule. "
        "If legacy result reproduction or provider guidance disagrees, prefer the known project behavior."
    )


if __name__ == "__main__":
    main()
