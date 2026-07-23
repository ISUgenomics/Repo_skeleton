import argparse
import csv
import re
import xml.etree.ElementTree as ET
from pathlib import Path
from zipfile import ZipFile

import pandas as pd
import yaml

from filter_and_Normalize import extractAbundanceData, filterLowPSM, read_provider_export
from helpers import (
    build_placeholder_comparisons,
    generate_comparisons_from_metadata,
    generate_sample_metadata_from_columns,
    prepare_manifest,
    renameColumns,
    sample_metadata_has_usable_labels,
    validate_comparisons_against_metadata,
    validate_sample_metadata_against_columns,
)


NS = "{http://schemas.openxmlformats.org/spreadsheetml/2006/main}"

SAMPLE_HEADER_ALIASES = [
    "sample_id",
    "sample id",
    "sample",
    "sample_name",
    "sample name",
    "sampleid",
    "sample column",
    "source_column",
    "source column",
]
GROUP_HEADER_ALIASES = ["group", "treatment_group", "treatment group", "combined_group", "combined group"]
NOTES_HEADER_ALIASES = ["notes", "note", "comments", "comment", "description", "details"]
BATCH_HEADER_ALIASES = ["batch", "run", "batch_or_run", "batch or run", "plate", "block"]
INCLUDE_HEADER_ALIASES = ["include", "use", "keep", "retain", "selected"]
PRIMARY_FACTOR_ALIASES = [
    "treatment",
    "diet",
    "condition",
    "grouping",
]
SECONDARY_FACTOR_ALIASES = [
    "challenge",
    "timepoint",
    "time_point",
    "time point",
    "sex",
    "genotype",
    "dose",
    "cohort",
    "status",
]


def normalize_header_label(value):
    return re.sub(r"[^a-z0-9]+", " ", str(value).strip().lower()).strip()


def read_cell_value(cell, shared_strings):
    cell_type = cell.attrib.get("t")
    if cell_type == "s":
        value = cell.find(NS + "v")
        return shared_strings[int(value.text)] if value is not None and value.text else ""
    if cell_type == "inlineStr":
        inline = cell.find(NS + "is")
        if inline is None:
            return ""
        return "".join((node.text or "") for node in inline.iter(NS + "t"))
    value = cell.find(NS + "v")
    return "" if value is None else (value.text or "")


def col_letters_to_index(letters):
    value = 0
    for char in letters:
        value = value * 26 + (ord(char.upper()) - 64)
    return value - 1


def load_xlsx_rows(path):
    rows = []
    with ZipFile(path) as archive:
        shared_strings = []
        if "xl/sharedStrings.xml" in archive.namelist():
            root = ET.fromstring(archive.read("xl/sharedStrings.xml"))
            for item in root.findall(NS + "si"):
                shared_strings.append("".join((node.text or "") for node in item.iter(NS + "t")))
        with archive.open("xl/worksheets/sheet1.xml") as handle:
            context = ET.iterparse(handle, events=("end",))
            for _, elem in context:
                if elem.tag != NS + "row":
                    continue
                current = []
                next_index = 0
                for cell in elem.findall(NS + "c"):
                    ref = cell.attrib.get("r", "")
                    if ref:
                        match = re.match(r"([A-Z]+)", ref)
                        col_index = col_letters_to_index(match.group(1)) if match else next_index
                    else:
                        col_index = next_index
                    while len(current) < col_index:
                        current.append("")
                    value = read_cell_value(cell, shared_strings).strip()
                    if len(current) == col_index:
                        current.append(value)
                    else:
                        current[col_index] = value
                    next_index = col_index + 1
                rows.append(current)
                elem.clear()
    return rows


def load_delimited_rows(path, delimiter):
    with open(path, "r", encoding="utf-8-sig", newline="") as handle:
        return [row for row in csv.reader(handle, delimiter=delimiter)]


def load_rows(path):
    suffix = path.suffix.lower()
    if suffix in {".xlsx", ".xls"}:
        return load_xlsx_rows(path)
    if suffix == ".csv":
        return load_delimited_rows(path, ",")
    if suffix in {".tsv", ".txt"}:
        return load_delimited_rows(path, "\t")
    raise ValueError(f"Unsupported metadata source format: {path}")


def normalize_rows(rows):
    max_len = max((len(row) for row in rows), default=0)
    normalized = []
    for row in rows:
        padded = [str(cell).strip() for cell in row] + [""] * (max_len - len(row))
        normalized.append(padded)
    return normalized


def extract_rows_with_header(path, header):
    rows = normalize_rows(load_rows(path))
    if header < 1 or header > len(rows):
        raise IndexError(f"header={header} is out of range for {path}")
    return rows[header - 1], rows[header:]


def detect_header_row(rows, source_columns=None):
    normalized_rows = normalize_rows(rows)
    source_set = {str(value).strip() for value in (source_columns or []) if str(value).strip()}
    best_index = 0
    best_score = -1
    max_scan = min(len(normalized_rows), 10)

    keyword_aliases = set(
        normalize_header_label(value)
        for value in (
            SAMPLE_HEADER_ALIASES
            + GROUP_HEADER_ALIASES
            + NOTES_HEADER_ALIASES
            + BATCH_HEADER_ALIASES
            + INCLUDE_HEADER_ALIASES
            + PRIMARY_FACTOR_ALIASES
            + SECONDARY_FACTOR_ALIASES
        )
    )

    for idx in range(max_scan):
        header = normalized_rows[idx]
        normalized_header = [normalize_header_label(cell) for cell in header]
        nonempty_header = [cell for cell in normalized_header if cell]
        if not nonempty_header:
            continue

        score = 0
        score += sum(6 for cell in nonempty_header if cell in keyword_aliases)
        if any(cell in {normalize_header_label(alias) for alias in SAMPLE_HEADER_ALIASES} for cell in nonempty_header):
            score += 20
        score += min(len(set(nonempty_header)), 8)

        preview_rows = normalized_rows[idx + 1 : idx + 6]
        if preview_rows:
            sample_like_hits = 0
            categorical_hits = 0
            for row in preview_rows:
                padded = row + [""] * max(0, len(header) - len(row))
                if source_set:
                    for value in padded:
                        if value.strip() in source_set:
                            sample_like_hits += 1
                categorical_hits += sum(1 for value in padded if value.strip())
            score += min(sample_like_hits, 12)
            score += min(categorical_hits // max(1, len(preview_rows)), 6)

        if score > best_score:
            best_score = score
            best_index = idx

    return best_index + 1


def resolve_column(selector, header):
    if not selector:
        return None
    selector = str(selector).strip()
    if selector.isdigit():
        idx = int(selector) - 1
        if idx < 0 or idx >= len(header):
            raise IndexError(f"Column number out of range: {selector}")
        return idx
    normalized = [str(name).strip() for name in header]
    if selector in normalized:
        return normalized.index(selector)
    lowered = [name.lower() for name in normalized]
    if selector.lower() in lowered:
        return lowered.index(selector.lower())
    raise KeyError(f"Column not found in header: {selector}")


def find_header_by_alias(header, aliases):
    normalized_header = [normalize_header_label(name) for name in header]
    alias_set = [normalize_header_label(alias) for alias in aliases]
    for alias in alias_set:
        if alias in normalized_header:
            return header[normalized_header.index(alias)]
    return ""


def infer_sample_selector(header, data_rows, source_columns=None):
    alias_match = find_header_by_alias(header, SAMPLE_HEADER_ALIASES)
    if alias_match:
        return alias_match

    source_set = {str(value).strip() for value in (source_columns or []) if str(value).strip()}
    best_idx = None
    best_overlap = -1
    if source_set:
        for idx, _ in enumerate(header):
            values = []
            for row in data_rows[:50]:
                if idx < len(row):
                    value = str(row[idx]).strip()
                    if value:
                        values.append(value)
            overlap = sum(1 for value in values if value in source_set)
            if overlap > best_overlap:
                best_overlap = overlap
                best_idx = idx
        if best_idx is not None and best_overlap > 0:
            return header[best_idx]

    return header[0] if header else ""


def infer_optional_selector(header, aliases):
    return find_header_by_alias(header, aliases)


def value_is_categorical(values):
    nonempty = [value for value in values if value]
    if not nonempty:
        return False
    unique = set(nonempty)
    if len(unique) == 1:
        return False
    if len(unique) > max(8, len(nonempty) // 2):
        return False
    mostly_numeric = sum(1 for value in nonempty if re.fullmatch(r"[-+]?\d+(\.\d+)?", value)) >= max(1, int(len(nonempty) * 0.8))
    return not mostly_numeric


def infer_factor_selectors(header, data_rows, reserved_headers=None):
    reserved = {normalize_header_label(value) for value in (reserved_headers or []) if value}
    treatment = infer_optional_selector(header, PRIMARY_FACTOR_ALIASES)
    factors = []
    if treatment:
        reserved.add(normalize_header_label(treatment))

    for alias in SECONDARY_FACTOR_ALIASES:
        match = find_header_by_alias(header, [alias])
        if match and normalize_header_label(match) not in reserved:
            factors.append((normalize_header_label(match).replace(" ", "_"), match))
            reserved.add(normalize_header_label(match))

    if not treatment:
        for idx, name in enumerate(header):
            normalized = normalize_header_label(name)
            if not normalized or normalized in reserved:
                continue
            values = [str(row[idx]).strip() for row in data_rows[:50] if idx < len(row)]
            if value_is_categorical(values):
                treatment = name
                reserved.add(normalized)
                break

    for idx, name in enumerate(header):
        normalized = normalize_header_label(name)
        if not normalized or normalized in reserved:
            continue
        if normalized in {
            normalize_header_label(value)
            for value in SAMPLE_HEADER_ALIASES + GROUP_HEADER_ALIASES + NOTES_HEADER_ALIASES + BATCH_HEADER_ALIASES + INCLUDE_HEADER_ALIASES
        }:
            continue
        values = [str(row[idx]).strip() for row in data_rows[:50] if idx < len(row)]
        if value_is_categorical(values):
            factors.append((normalized.replace(" ", "_"), name))
            reserved.add(normalized)

    deduped = []
    seen = set()
    for name, selector in factors:
        if name not in seen:
            deduped.append((name, selector))
            seen.add(name)
    return treatment, deduped


def infer_external_metadata_mapping(path, source_columns=None):
    rows = load_rows(path)
    detected_header = detect_header_row(rows, source_columns=source_columns)
    header_row, data_rows = extract_rows_with_header(path, detected_header)
    sample = infer_sample_selector(header_row, data_rows, source_columns=source_columns)
    source = sample
    group = infer_optional_selector(header_row, GROUP_HEADER_ALIASES)
    batch = infer_optional_selector(header_row, BATCH_HEADER_ALIASES)
    include = infer_optional_selector(header_row, INCLUDE_HEADER_ALIASES)
    notes = infer_optional_selector(header_row, NOTES_HEADER_ALIASES)
    treatment, factor_specs = infer_factor_selectors(
        header_row,
        data_rows,
        reserved_headers=[sample, source, group, batch, include, notes],
    )
    if treatment:
        factor_specs = [(name, selector) for name, selector in factor_specs if normalize_header_label(selector) != normalize_header_label(treatment)]
    return {
        "header": detected_header,
        "sample": sample,
        "source": source,
        "treatment": treatment,
        "factor_specs": [f"{name}={selector}" for name, selector in factor_specs],
        "group": group,
        "batch": batch,
        "include": include,
        "notes": notes,
    }


def parse_bool(value, default=True):
    if value == "":
        return default
    return str(value).strip().lower() in {"true", "1", "yes", "y"}


def read_context_text_files(project_root):
    raw_dir = project_root / "workflow" / "00_raw_data"
    chunks = []
    for path in sorted(raw_dir.glob("*.txt")):
        if not path.is_file():
            continue
        try:
            chunks.append(path.read_text(encoding="utf-8"))
        except Exception:
            continue
    return "\n".join(chunks)


def extract_requested_pairs(text):
    pairs = []
    seen = set()
    for left, right in re.findall(r"\b([A-Za-z0-9_-]+)\s+vs\.?\s+([A-Za-z0-9_-]+)\b", text or "", flags=re.IGNORECASE):
        left = left.strip()
        right = right.strip()
        key = tuple(sorted([left.upper(), right.upper()]))
        if left and right and key not in seen:
            pairs.append((left, right))
            seen.add(key)
    return pairs


def infer_grouping_column_for_pair(sample_metadata, left, right):
    candidate_columns = []
    for column in sample_metadata.columns:
        if column in {"sample_id", "source_column", "replicate", "batch_or_run", "include", "notes"}:
            continue
        values = {str(value).strip() for value in sample_metadata[column].dropna().astype(str) if str(value).strip()}
        if left in values and right in values:
            candidate_columns.append(column)
    preferred_order = ["treatment", "challenge", "group"]
    for preferred in preferred_order:
        if preferred in candidate_columns:
            return preferred
    return candidate_columns[0] if candidate_columns else ""


def build_requested_comparison_specs(sample_metadata, text):
    specs = []
    for left, right in extract_requested_pairs(text):
        grouping_column = infer_grouping_column_for_pair(sample_metadata, left, right)
        if not grouping_column:
            continue
        specs.append(
            {
                "comparison_id": f"{left}_vs_{right}",
                "grouping_column": grouping_column,
                "group1": left,
                "group2": right,
            }
        )
    return specs


def filter_comparisons_to_requested(sample_metadata, comparisons, requested_specs):
    if comparisons.empty or not requested_specs:
        return comparisons
    requested_lookup = {
        (
            spec["grouping_column"],
            tuple(sorted([spec["group1"], spec["group2"]])),
        ): spec
        for spec in requested_specs
    }
    kept_rows = []
    for _, row in comparisons.iterrows():
        grouping = str(row.get("grouping_column", "")).strip()
        pair = tuple(sorted([str(row.get("group1", "")).strip(), str(row.get("group2", "")).strip()]))
        spec = requested_lookup.get((grouping, pair))
        if not spec:
            continue
        row_copy = row.copy()
        row_copy["comparison_id"] = spec["comparison_id"]
        row_copy["group1"] = spec["group1"]
        row_copy["group2"] = spec["group2"]
        kept_rows.append(row_copy)
    if not kept_rows:
        return comparisons
    filtered = pd.DataFrame(kept_rows, columns=comparisons.columns)
    filtered = filtered.drop_duplicates(subset=["comparison_id", "grouping_column", "group1", "group2"]).reset_index(drop=True)
    return filtered


def parse_factor_specs(factor_specs, treatment_selector=""):
    parsed = []
    if treatment_selector:
        parsed.append(("treatment", treatment_selector))
    for spec in factor_specs or []:
        if "=" not in spec:
            raise ValueError(f"Invalid --factor value: {spec}. Use name=column_name or name=column_number.")
        name, selector = spec.split("=", 1)
        name = name.strip()
        selector = selector.strip()
        if not name or not selector:
            raise ValueError(f"Invalid --factor value: {spec}. Use name=column_name or name=column_number.")
        parsed.append((name, selector))
    seen = set()
    deduped = []
    for name, selector in parsed:
        if name in seen:
            raise ValueError(f"Duplicate factor name: {name}")
        deduped.append((name, selector))
        seen.add(name)
    return deduped


def build_output_rows(
    header,
    data_rows,
    sample_selector,
    source_selector="",
    factor_specs=None,
    group_selector="",
    batch_selector="",
    include_selector="",
    notes_selector="",
):
    factor_specs = factor_specs or []
    sample_idx = resolve_column(sample_selector, header)
    source_idx = resolve_column(source_selector, header) if source_selector else sample_idx
    group_idx = resolve_column(group_selector, header) if group_selector else None
    batch_idx = resolve_column(batch_selector, header) if batch_selector else None
    include_idx = resolve_column(include_selector, header) if include_selector else None
    notes_idx = resolve_column(notes_selector, header) if notes_selector else None
    factor_indexes = [(name, resolve_column(selector, header)) for name, selector in factor_specs]

    output_rows = []
    for row in data_rows:
        row = row + [""] * max(0, len(header) - len(row))
        sample_id = row[sample_idx].strip()
        if sample_id == "":
            continue
        factor_values = {}
        for name, idx in factor_indexes:
            factor_values[name] = row[idx].strip()
        group = row[group_idx].strip() if group_idx is not None else ""
        if group == "":
            group_parts = [factor_values[name] for name, _ in factor_indexes if factor_values[name]]
            group = "-".join(group_parts)
        output_row = {
            "sample_id": sample_id,
            "source_column": row[source_idx].strip() or sample_id,
            "group": group,
            "batch_or_run": row[batch_idx].strip() if batch_idx is not None else "",
            "include": parse_bool(row[include_idx].strip(), default=True) if include_idx is not None else True,
            "notes": row[notes_idx].strip() if notes_idx is not None else "",
        }
        for name, value in factor_values.items():
            output_row[name] = value
        output_rows.append(output_row)
    return output_rows


def add_replicates(rows, factor_names):
    counters = {}
    for row in rows:
        key_parts = [row.get("group", "").strip()]
        if not key_parts[0]:
            key_parts = [row.get(name, "").strip() for name in factor_names if row.get(name, "").strip()]
        key = "|".join(key_parts) if any(key_parts) else "all_samples"
        counters[key] = counters.get(key, 0) + 1
        row["replicate"] = counters[key]


def ensure_unique_sample_ids(rows):
    seen = set()
    duplicates = []
    for row in rows:
        sample_id = row["sample_id"]
        if sample_id in seen:
            duplicates.append(sample_id)
        seen.add(sample_id)
    if duplicates:
        raise ValueError(f"Duplicate sample_id values found: {sorted(set(duplicates))}")


def output_fieldnames(rows):
    factor_names = []
    for row in rows:
        for key in row:
            if key not in {"sample_id", "source_column", "group", "replicate", "batch_or_run", "include", "notes"} and key not in factor_names:
                factor_names.append(key)
    return ["sample_id", "source_column", *factor_names, "group", "replicate", "batch_or_run", "include", "notes"]


def write_sample_metadata(output_path, rows):
    output_path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = output_fieldnames(rows)
    with open(output_path, "w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            row_copy = dict(row)
            row_copy["include"] = "TRUE" if row_copy["include"] else "FALSE"
            writer.writerow(row_copy)
    return fieldnames


def build_source_columns(project_root, input_cfg, analysis_cfg):
    data_path = project_root / input_cfg["provider_export"]
    data = read_provider_export(
        data_path,
        input_format=analysis_cfg.get("input_format", "xlsx"),
        index_col=int(analysis_cfg.get("input_index_column", 4)),
    )
    filtered_data = filterLowPSM(
        data,
        psm_value=int(analysis_cfg.get("psm_threshold", 3)),
        controlColumnContains=analysis_cfg.get("psm_column_contains", "PSM"),
    )
    abundance_data = extractAbundanceData(
        filtered_data,
        abundanceColumnContains=analysis_cfg.get("abundance_column_contains", "Abundances (Grouped):"),
    )
    renameColumns(
        abundance_data,
        regexes=analysis_cfg.get("column_rename_regexes", [r"Abundances_\(Grouped\):_", r"_Female"]),
    )
    return abundance_data.columns.tolist()


def load_manifest_info(manifest_path):
    with open(manifest_path, "r", encoding="utf-8") as handle:
        manifest = yaml.safe_load(handle)
    project_root = manifest_path.parents[3]
    _, input_cfg, analysis_cfg, _, _ = prepare_manifest(manifest)
    return {
        "project_root": project_root,
        "input_cfg": input_cfg,
        "analysis_cfg": analysis_cfg,
        "raw_data_path": project_root / input_cfg["provider_export"] if input_cfg.get("provider_export") else None,
        "metadata_source_path": project_root / input_cfg["metadata_source"] if input_cfg.get("metadata_source") else None,
        "sample_metadata_path": project_root / input_cfg["sample_metadata_csv"],
        "comparisons_path": project_root / input_cfg["comparisons_csv"],
        "comparisons_mode": str(input_cfg.get("comparisons_mode", "generated")).strip().lower(),
    }


def dataframe_from_rows(rows):
    fieldnames = output_fieldnames(rows)
    return pd.DataFrame(rows, columns=fieldnames)


def default_comparisons_path(output_path):
    return output_path.with_name("comparisons.csv")


def run_pipeline(
    manifest="",
    input_path="",
    output_path="",
    header=1,
    sample="",
    source="",
    treatment="",
    factor_specs=None,
    group="",
    batch="",
    include="",
    notes="",
    generate_comparisons=True,
    force=False,
):
    manifest_info = load_manifest_info(Path(manifest).resolve()) if manifest else None
    factor_specs = factor_specs or []

    resolved_input = Path(input_path).resolve() if input_path else (
        manifest_info["metadata_source_path"] if manifest_info else None
    )
    resolved_output = Path(output_path).resolve() if output_path else (
        manifest_info["sample_metadata_path"] if manifest_info else Path("workflow/00_raw_data/config/sample_metadata.csv").resolve()
    )
    comparisons_path = manifest_info["comparisons_path"] if manifest_info else default_comparisons_path(resolved_output)
    comparisons_mode = manifest_info["comparisons_mode"] if manifest_info else "generated"
    project_context_text = read_context_text_files(manifest_info["project_root"]) if manifest_info else ""

    if resolved_input and resolved_input.exists():
        inferred = None
        if not sample:
            inferred = infer_external_metadata_mapping(
                resolved_input,
                source_columns=(
                    build_source_columns(
                        manifest_info["project_root"],
                        manifest_info["input_cfg"],
                        manifest_info["analysis_cfg"],
                    )
                    if manifest_info and manifest_info["raw_data_path"] and manifest_info["raw_data_path"].exists()
                    else None
                ),
            )
            header = inferred["header"]
            sample = inferred["sample"]
            source = source or inferred["source"]
            treatment = treatment or inferred["treatment"]
            factor_specs = factor_specs or inferred["factor_specs"]
            group = group or inferred["group"]
            batch = batch or inferred["batch"]
            include = include or inferred["include"]
            notes = notes or inferred["notes"]
        factor_specs = parse_factor_specs(factor_specs or [], treatment_selector=treatment)
        if resolved_output.exists() and not force:
            raise FileExistsError(
                f"{resolved_output} already exists. Re-run with --force to replace it from the metadata source file."
            )
        if not sample:
            raise ValueError("--sample is required when reading an external metadata source file.")
        header_row, data_rows = extract_rows_with_header(resolved_input, header)
        output_rows = build_output_rows(
            header_row,
            data_rows,
            sample_selector=sample,
            source_selector=source,
            factor_specs=factor_specs,
            group_selector=group,
            batch_selector=batch,
            include_selector=include,
            notes_selector=notes,
        )
        ensure_unique_sample_ids(output_rows)
        add_replicates(output_rows, [name for name, _ in factor_specs])
        sample_metadata = dataframe_from_rows(output_rows)
    elif manifest_info and manifest_info["raw_data_path"] and manifest_info["raw_data_path"].exists():
        if resolved_output.exists() and not force:
            sample_metadata = pd.read_csv(resolved_output)
        else:
            source_columns = build_source_columns(
                manifest_info["project_root"],
                manifest_info["input_cfg"],
                manifest_info["analysis_cfg"],
            )
            sample_metadata = generate_sample_metadata_from_columns(source_columns)
    else:
        raise FileNotFoundError(
            "No metadata source file was found and no manifest-defined raw data file could be used. "
            "Provide --input or set inputs.metadata_source / inputs.raw_data_file in project_manifest.yaml."
        )

    source_columns = None
    if manifest_info and manifest_info["raw_data_path"] and manifest_info["raw_data_path"].exists():
        source_columns = build_source_columns(
            manifest_info["project_root"],
            manifest_info["input_cfg"],
            manifest_info["analysis_cfg"],
        )
        validate_sample_metadata_against_columns(sample_metadata, source_columns)

    resolved_output.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = write_sample_metadata(resolved_output, sample_metadata.to_dict(orient="records"))

    result = {
        "sample_metadata_path": resolved_output,
        "sample_metadata_columns": fieldnames,
        "comparisons_path": comparisons_path,
        "comparisons_mode": comparisons_mode,
        "metadata_ready": sample_metadata_has_usable_labels(sample_metadata),
        "comparisons_written": False,
        "comparisons_validated": False,
    }

    if not generate_comparisons:
        return result

    comparisons_path.parent.mkdir(parents=True, exist_ok=True)
    if result["metadata_ready"]:
        if comparisons_mode == "manual" and comparisons_path.exists() and not force:
            comparisons = pd.read_csv(comparisons_path)
            validate_comparisons_against_metadata(comparisons, sample_metadata)
            result["comparisons_validated"] = True
        else:
            comparisons = generate_comparisons_from_metadata(sample_metadata)
            requested_specs = build_requested_comparison_specs(sample_metadata, project_context_text)
            comparisons = filter_comparisons_to_requested(sample_metadata, comparisons, requested_specs)
            if comparisons.empty:
                comparisons = build_placeholder_comparisons()
            comparisons.to_csv(comparisons_path, index=False)
            result["comparisons_written"] = True
    else:
        if not comparisons_path.exists() or force:
            build_placeholder_comparisons().to_csv(comparisons_path, index=False)
            result["comparisons_written"] = True

    return result


def main(argv=None):
    parser = argparse.ArgumentParser(
        description="Create sample_metadata.csv and, by default, comparisons.csv from a metadata file or manifest-defined raw data."
    )
    parser.add_argument("--manifest", default="", help="Optional project_manifest.yaml used to resolve defaults and validate sample columns.")
    parser.add_argument("--input", default="", help="Metadata source file (.xlsx, .csv, .tsv, .txt). If omitted, fall back to inputs.metadata_source or raw-data starter generation.")
    parser.add_argument("--output", default="", help="Output sample_metadata.csv path.")
    parser.add_argument("--header", type=int, default=1, help="1-based header row number in the metadata source file.")
    parser.add_argument("--sample", default="", help="Header name or 1-based column number for sample_id.")
    parser.add_argument("--source", default="", help="Optional header name or 1-based column number for source_column. Defaults to --sample.")
    parser.add_argument("--treatment", default="", help="Optional header name or 1-based column number for the primary treatment factor.")
    parser.add_argument("--factor", action="append", default=[], help="Additional factor mapping in the form name=column_name or name=column_number. Repeat as needed.")
    parser.add_argument("--group", default="", help="Optional header name or 1-based column number for group. If omitted, group is built by joining factor values.")
    parser.add_argument("--batch", default="", help="Optional header name or 1-based column number for batch_or_run.")
    parser.add_argument("--include", default="", help="Optional header name or 1-based column number for include.")
    parser.add_argument("--notes", default="", help="Optional header name or 1-based column number for notes/comments.")
    parser.add_argument("--no-comparisons", action="store_true", help="Write sample_metadata.csv only and skip comparisons.csv handling.")
    parser.add_argument("--force", action="store_true", help="Overwrite existing sample_metadata.csv and auto-generated comparisons.csv.")
    args = parser.parse_args(argv)

    result = run_pipeline(
        manifest=args.manifest,
        input_path=args.input,
        output_path=args.output,
        header=args.header,
        sample=args.sample,
        source=args.source,
        treatment=args.treatment,
        factor_specs=args.factor,
        group=args.group,
        batch=args.batch,
        include=args.include,
        notes=args.notes,
        generate_comparisons=not args.no_comparisons,
        force=args.force,
    )

    print(f"Wrote {result['sample_metadata_path']}")
    print(f"Columns written: {', '.join(result['sample_metadata_columns'])}")

    if args.no_comparisons:
        return

    if result["comparisons_validated"]:
        print(f"Validated existing {result['comparisons_path']} (comparisons_mode=manual)")
    elif result["comparisons_written"]:
        print(f"Wrote {result['comparisons_path']}")

    if result["metadata_ready"]:
        print("Metadata labels are usable for comparison generation and notebook validation.")
    else:
        print(
            "Metadata still needs manual correction before real comparisons can run. "
            f"Review {result['sample_metadata_path']} and rerun metadata_gen.py when ready."
        )


if __name__ == "__main__":
    main()
