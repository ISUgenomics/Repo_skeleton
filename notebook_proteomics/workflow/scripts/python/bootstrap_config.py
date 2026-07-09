import argparse
from pathlib import Path

import pandas as pd
import yaml

from helpers import renameColumns


def load_legacy_metadata(path):
    path = Path(path)
    if path.suffix.lower() in {".csv", ".txt", ".tsv"}:
        df = pd.read_csv(path, sep=None, engine="python")
    elif path.suffix.lower() in {".xlsx", ".xls"}:
        df = pd.read_excel(path)
    else:
        raise ValueError(f"Unsupported legacy metadata format: {path}")
    return df


def extract_source_columns(input_file, abundance_column_contains, rename_regexes):
    header_df = pd.read_excel(input_file, nrows=0)
    abundance_columns = [c for c in header_df.columns if abundance_column_contains in str(c)]
    renamed = pd.DataFrame(columns=abundance_columns)
    renameColumns(renamed, regexes=rename_regexes)
    return renamed.columns.tolist()


def build_sample_metadata(source_columns, legacy_metadata=None):
    rows = []
    legacy_by_sample = {}
    if legacy_metadata is not None and "sample" in legacy_metadata.columns:
        legacy_by_sample = {
            str(row["sample"]): row for _, row in legacy_metadata.iterrows()
        }

    replicate_counter = {}
    for source_column in source_columns:
        parts = str(source_column).split("_")
        sample_id = parts[1] if len(parts) > 1 else source_column
        legacy_row = legacy_by_sample.get(sample_id, {})
        treatment = legacy_row.get("treatment", "")
        group = legacy_row.get("group", "")
        batch = legacy_row.get("file", parts[0] if parts else "")
        replicate_key = (treatment, group)
        replicate_counter[replicate_key] = replicate_counter.get(replicate_key, 0) + 1
        rows.append(
            {
                "sample_id": sample_id,
                "source_column": source_column,
                "treatment": treatment,
                "group": group,
                "replicate": replicate_counter[replicate_key],
                "batch_or_run": batch,
                "include": True,
                "notes": "",
            }
        )

    return pd.DataFrame(rows)


def build_manifest(args):
    return {
        "project": {
            "project_id": args.project_id,
            "project_title": args.project_title,
            "organism": args.organism,
            "material": args.material,
            "analysis_owner": args.analysis_owner,
        },
        "inputs": {
            "provider_export": args.input_file,
            "cleaned_export": "",
            "metadata_source": args.legacy_metadata or "",
            "sample_metadata_csv": "workflow/00_raw_data/config/sample_metadata.csv",
            "comparisons_csv": "workflow/00_raw_data/config/comparisons.csv",
        },
        "analysis": {
            "notebook_name": "proteomics_analysis.ipynb",
            "data_mode": "grouped",
            "provider_type": args.provider_type,
            "input_format": Path(args.input_file).suffix.lstrip(".").lower(),
            "input_index_column": args.input_index_column,
            "psm_column_contains": args.psm_column_contains,
            "abundance_column_contains": args.abundance_column_contains,
            "column_rename_regexes": args.rename_regexes,
            "grouping_column": "group",
            "psm_threshold": args.psm_threshold,
            "remove_zero_only_rows": True,
            "normalization_primary": args.normalization_primary,
            "normalization_secondary": args.normalization_secondary,
            "statistic": "student_t_test",
            "multiple_testing": "fdr_bh",
            "apply_uq_per_comparison": True,
        },
        "outputs": {
            "qc_dir": "workflow/01_qc_normalization",
            "results_dir": "workflow/02_statistics",
            "plots_dir": "workflow/03_visualization",
            "secondary_dir": "workflow/04_secondary_analyses",
            "final_report_dir": "workflow/final_report",
            "scripts_dir": "workflow/scripts",
        },
        "flags": {
            "astral_mode": False,
            "use_prtc": True,
            "generate_qvalue_plots": True,
        },
    }


def main():
    parser = argparse.ArgumentParser(description="Bootstrap proteomics template config from a provider export.")
    parser.add_argument("--project-root", default=".", help="Path to the copied notebook_proteomics project root")
    parser.add_argument("--input-file", required=True, help="Provider export path relative to the project root")
    parser.add_argument("--legacy-metadata", help="Optional existing metadata.txt/.csv/.xlsx file to map treatment and group")
    parser.add_argument("--project-id", default="fill_in_project_id")
    parser.add_argument("--project-title", default="fill_in_project_title")
    parser.add_argument("--organism", default="fill_in_organism")
    parser.add_argument("--material", default="fill_in_material")
    parser.add_argument("--analysis-owner", default="fill_in_analysis_owner")
    parser.add_argument("--provider-type", default="Thermo Proteome Discoverer export")
    parser.add_argument("--input-index-column", type=int, default=4)
    parser.add_argument("--psm-column-contains", default="PSM")
    parser.add_argument("--abundance-column-contains", default="Abundances (Grouped):")
    parser.add_argument("--rename-regexes", nargs="+", default=[r"Abundances_\(Grouped\):_", r"_Female"])
    parser.add_argument("--psm-threshold", type=int, default=3)
    parser.add_argument("--normalization-primary", default="fill_in_primary_normalization")
    parser.add_argument("--normalization-secondary", default="optional")
    parser.add_argument("--force", action="store_true", help="Overwrite existing manifest and sample metadata files")
    args = parser.parse_args()

    project_root = Path(args.project_root).resolve()
    input_file = project_root / args.input_file
    config_dir = project_root / "workflow" / "00_raw_data" / "config"
    config_dir.mkdir(parents=True, exist_ok=True)

    legacy_metadata = load_legacy_metadata(project_root / args.legacy_metadata) if args.legacy_metadata else None
    source_columns = extract_source_columns(input_file, args.abundance_column_contains, args.rename_regexes)
    sample_metadata = build_sample_metadata(source_columns, legacy_metadata=legacy_metadata)
    manifest = build_manifest(args)

    manifest_path = config_dir / "project_manifest.yaml"
    sample_metadata_path = config_dir / "sample_metadata.csv"
    if not args.force:
        for path in [manifest_path, sample_metadata_path]:
            if path.exists():
                raise FileExistsError(f"{path} already exists. Re-run with --force to overwrite it.")

    with open(manifest_path, "w", encoding="utf-8") as handle:
        yaml.safe_dump(manifest, handle, sort_keys=False)
    sample_metadata.to_csv(sample_metadata_path, index=False)

    comparisons_path = config_dir / "comparisons.csv"
    if not comparisons_path.exists():
        pd.DataFrame(
            columns=[
                "comparison_id",
                "grouping_column",
                "group1",
                "group2",
                "use_qvalue",
                "pvalue_cutoff",
                "qvalue_cutoff",
                "abs_log2fc_cutoff",
                "enabled",
                "notes",
            ]
        ).to_csv(comparisons_path, index=False)

    print(f"Wrote {manifest_path}")
    print(f"Wrote {sample_metadata_path}")
    print(f"Prepared {comparisons_path}")


if __name__ == "__main__":
    main()
