import argparse
from pathlib import Path
import re

import pandas as pd
import yaml

from infer_astral_mode import build_recommendation, summarize_xlsx_visible_master_rows


RAW_FILE_PATTERNS = [
    "*.xlsx",
    "*.xls",
    "*.csv",
    "*.txt",
    "*.tsv",
]

CONTEXT_TEXT_PATTERNS = ["*.txt"]

ORGANISM_PATTERNS = [
    (r"\b(bovine|bos taurus|holstein|cow|cows|cattle)\b", "Bos taurus"),
    (r"\b(human|homo sapiens)\b", "Homo sapiens"),
    (r"\b(mouse|mice|mus musculus)\b", "Mus musculus"),
    (r"\b(rat|rats|rattus norvegicus)\b", "Rattus norvegicus"),
    (r"\b(pig|pigs|sus scrofa|porcine)\b", "Sus scrofa"),
    (r"\b(sheep|ovine|ovis aries)\b", "Ovis aries"),
    (r"\b(goat|goats|capra hircus)\b", "Capra hircus"),
    (r"\b(chicken|gallus gallus)\b", "Gallus gallus"),
]

MATERIAL_PATTERNS = [
    "mammary tissue",
    "mammary gland",
    "mammary proteome",
    "milk",
    "plasma",
    "serum",
    "liver",
    "muscle",
    "kidney",
    "brain",
    "heart",
    "lung",
    "adipose tissue",
    "adipose",
]


def yaml_scalar(value):
    dumped = yaml.safe_dump(value, default_flow_style=True, sort_keys=False).strip()
    return "\n".join(line for line in dumped.splitlines() if line.strip() != "...")


def render_manifest_with_comments(manifest):
    project = manifest["project"]
    inputs = manifest["inputs"]
    analysis = manifest["analysis"]
    column_rename_regexes = analysis.get("column_rename_regexes", [])
    merge_operations = analysis.get("post_normalization_column_merges", [])

    lines = [
        "# Edit this file in place before running the notebook.",
        "# Keep paths relative to the copied notebook_proteomics project root.",
        "# Keep it short: only include fields needed to start and control the analysis.",
        "",
        "project:",
        f"  project_id: {yaml_scalar(project['project_id'])}  # Stable short ID; usually the project code or folder name.",
        f"  project_title: {yaml_scalar(project['project_title'])}  # Human-readable study title used in reports and docs.",
        f"  organism: {yaml_scalar(project['organism'])}  # Species or biological system, for example \"Bos taurus\".",
        f"  material: {yaml_scalar(project['material'])}  # Tissue, fluid, or sample type, for example \"liver proteomics\".",
        f"  analysis_owner: {yaml_scalar(project['analysis_owner'])}  # Person or workflow label responsible for this run.",
        "",
        "inputs:",
        f"  raw_data_file: {yaml_scalar(inputs['raw_data_file'])}  # Main raw data file used to start the analysis.",
        f"  metadata_source: {yaml_scalar(inputs['metadata_source'])}  # Optional legacy metadata/reference file; leave empty if none.",
        f"  sample_metadata_csv: {yaml_scalar(inputs['sample_metadata_csv'])}  # Sample annotations used for grouping and inclusion.",
        f"  comparisons_csv: {yaml_scalar(inputs['comparisons_csv'])}  # Comparison definitions and cutoffs.",
        f"  comparisons_mode: {yaml_scalar(inputs['comparisons_mode'])}  # Use generated to let the workflow create/update comparisons from sample_metadata.csv, or manual to preserve a hand-curated comparisons.csv.",
        "",
        "analysis:",
        f"  input_format: {yaml_scalar(analysis['input_format'])}  # Must match the raw data file type: xlsx, xls, csv, txt, or tsv.",
        f"  input_index_column: {yaml_scalar(analysis['input_index_column'])}  # Zero-based index of the protein/accession identifier column in the source file.",
        f"  psm_threshold: {yaml_scalar(analysis['psm_threshold'])}  # Minimum PSM count required to keep a protein row.",
        f"  psm_column_contains: {yaml_scalar(analysis['psm_column_contains'])}  # Substring used to locate the PSM/count column in the export.",
        f"  abundance_column_contains: {yaml_scalar(analysis['abundance_column_contains'])}  # Substring used to locate abundance/sample columns.",
        "  column_rename_regexes:  # Regexes removed from abundance column names before matching sample metadata.",
    ]

    for idx, regex in enumerate(column_rename_regexes):
        if idx == 0:
            comment = "  # Common Proteome Discoverer grouped-abundance prefix."
        elif idx == 1:
            comment = "  # Example suffix to strip; replace or remove to match your sample names."
        else:
            comment = ""
        lines.append(f"    - {yaml_scalar(regex)}{comment}")

    lines.extend([
        f"  grouping_column: {yaml_scalar(analysis['grouping_column'])}  # Default sample_metadata.csv column used when comparisons.csv does not override grouping_column.",
        f"  normalization_primary: {yaml_scalar(analysis['normalization_primary'])}  # Required; common values are PRTC, control_run_quartile, or none.",
        f"  normalization_secondary: {yaml_scalar(analysis['normalization_secondary'])}  # Optional secondary normalization label or note for reporting.",
        f"  apply_uq_per_comparison: {yaml_scalar(analysis['apply_uq_per_comparison'])}  # Apply upper-quartile normalization within each comparison before statistics.",
        f"  astral_mode: {yaml_scalar(analysis['astral_mode'])}  # Set true only when zeros should be treated as missing-value placeholders during t-test filtering.",
        f"  between_group_bias_mode: {yaml_scalar(analysis['between_group_bias_mode'])}  # Usually leave as none; change only for a validated legacy bias-handling mode.",
        f"  run_block_size: {yaml_scalar(analysis['run_block_size'])}  # Samples per run block for control_run_quartile normalization.",
        f"  control_column_contains: {yaml_scalar(analysis['control_column_contains'])}  # Substring that identifies the control channel for control_run_quartile.",
    ])

    if merge_operations:
        lines.append("  post_normalization_column_merges:  # Optional technical-replicate merges after normalization.")
        for merge_op in merge_operations:
            lines.append(f"    - output_column: {yaml_scalar(merge_op['output_column'])}")
            lines.append("      input_columns:")
            for input_col in merge_op.get("input_columns", []):
                lines.append(f"        - {yaml_scalar(input_col)}")
            lines.append(f"      method: {yaml_scalar(merge_op.get('method', 'nonzero_mean'))}")
            lines.append(f"      drop_inputs: {yaml_scalar(merge_op.get('drop_inputs', True))}")
    else:
        lines.append("  post_normalization_column_merges: []  # Optional technical-replicate merges after normalization; leave [] if not needed.")

    lines.append(f"  generate_qvalue_plots: {yaml_scalar(analysis['generate_qvalue_plots'])}  # Also create q-value-based plots when q-values are available.")
    lines.append("")
    return "\n".join(lines)


def read_input_file(path, index_col):
    suffix = path.suffix.lower()
    if suffix in {".xlsx", ".xls"}:
        return pd.read_excel(path, index_col=index_col)
    if suffix == ".csv":
        return pd.read_csv(path, index_col=index_col)
    if suffix in {".txt", ".tsv"}:
        return pd.read_csv(path, sep="\t", index_col=index_col)
    raise ValueError(f"Unsupported input file format: {path}")


def find_raw_data_file(raw_dir):
    candidates = []
    for pattern in RAW_FILE_PATTERNS:
        candidates.extend(sorted(raw_dir.glob(pattern)))
    candidates = [p for p in candidates if p.is_file()]
    if not candidates:
        raise FileNotFoundError(f"No raw data file found in {raw_dir}")
    preferred = [p for p in candidates if "visible" in p.name.lower() or "visonly" in p.name.lower()]
    return preferred[0] if preferred else candidates[0]


def find_metadata_source(raw_dir):
    candidates = sorted(
        p for p in raw_dir.iterdir()
        if p.is_file()
        and any(token in p.name.lower() for token in ["metadata", "treatment", "design"])
        and p.name.lower() not in {"sample_metadata.csv", "comparisons.csv", "project_manifest.yaml"}
    )
    return candidates[0] if candidates else None


def detect_prtc(path, index_col):
    try:
        df = read_input_file(path, index_col=index_col)
    except Exception:
        return False
    return df.index.astype(str).str.startswith("PRTC-").any()


def infer_astral_mode_value(path, default=True):
    if path.suffix.lower() != ".xlsx":
        return default
    try:
        summary = summarize_xlsx_visible_master_rows(path)
        recommendation = build_recommendation(summary)
        return bool(recommendation["value"])
    except Exception:
        return default


def read_context_text(raw_dir):
    chunks = []
    for pattern in CONTEXT_TEXT_PATTERNS:
        for path in sorted(raw_dir.glob(pattern)):
            if path.is_file():
                try:
                    chunks.append(path.read_text(encoding="utf-8"))
                except Exception:
                    continue
    return "\n".join(chunks)


def read_tabular_text(path):
    if not path or not path.exists():
        return ""
    suffix = path.suffix.lower()
    try:
        if suffix in {".xlsx", ".xls"}:
            frame = pd.read_excel(path, header=None)
        elif suffix == ".csv":
            frame = pd.read_csv(path, header=None)
        elif suffix in {".txt", ".tsv"}:
            frame = pd.read_csv(path, header=None, sep="\t")
        else:
            return ""
    except Exception:
        return ""
    values = []
    for row in frame.head(50).fillna("").astype(str).itertuples(index=False):
        for value in row:
            value = value.strip()
            if value:
                values.append(value)
    return "\n".join(values)


def infer_organism_from_text(text):
    lowered = text.lower()
    for pattern, label in ORGANISM_PATTERNS:
        if re.search(pattern, lowered):
            return label
    return ""


def infer_material_from_text(text):
    lowered = text.lower()
    for label in MATERIAL_PATTERNS:
        if label in lowered:
            return label
    return ""


def infer_analysis_owner_from_text(text):
    patterns = [
        r"let'?s have ([A-Z][a-z]+) take lead",
        r"have ([A-Z][a-z]+) take lead",
        r"([A-Z][a-z]+) can lead",
    ]
    for pattern in patterns:
        match = re.search(pattern, text)
        if match:
            return match.group(1)
    return ""


def infer_manifest(project_root, project_id="", project_title="", organism="", material="", analysis_owner=""):
    raw_dir = project_root / "workflow" / "00_raw_data"
    raw_file = find_raw_data_file(raw_dir)
    metadata_source = find_metadata_source(raw_dir)
    context_text = read_context_text(raw_dir)
    if metadata_source:
        context_text = "\n".join(filter(None, [context_text, read_tabular_text(metadata_source)]))
    input_format = raw_file.suffix.lstrip(".").lower()
    input_index_column = 4 if input_format in {"xlsx", "xls", "csv"} else 3
    has_prtc = detect_prtc(raw_file, index_col=input_index_column)
    astral_mode = infer_astral_mode_value(raw_file, default=True)
    inferred_organism = infer_organism_from_text(context_text)
    inferred_material = infer_material_from_text(context_text)
    inferred_owner = infer_analysis_owner_from_text(context_text)

    return {
        "project": {
            "project_id": project_id or project_root.name,
            "project_title": project_title or project_root.name.replace("_", " ").strip(),
            "organism": organism or inferred_organism or "fill_in_organism",
            "material": material or inferred_material or "fill_in_material",
            "analysis_owner": analysis_owner or inferred_owner or "fill_in_analysis_owner",
        },
        "inputs": {
            "raw_data_file": str(raw_file.relative_to(project_root)),
            "metadata_source": str(metadata_source.relative_to(project_root)) if metadata_source else "",
            "sample_metadata_csv": "workflow/00_raw_data/config/sample_metadata.csv",
            "comparisons_csv": "workflow/00_raw_data/config/comparisons.csv",
            "comparisons_mode": "generated",
        },
        "analysis": {
            "input_format": input_format,
            "input_index_column": input_index_column,
            "psm_threshold": 3,
            "psm_column_contains": "PSM",
            "abundance_column_contains": "Abundances (Grouped):",
            "column_rename_regexes": [r"Abundances_\(Grouped\):_", r"_Female"],
            "grouping_column": "group",
            "normalization_primary": "PRTC" if has_prtc else "fill_in_primary_normalization",
            "normalization_secondary": "optional",
            "apply_uq_per_comparison": True,
            "astral_mode": astral_mode,
            "between_group_bias_mode": "none",
            "run_block_size": 11,
            "control_column_contains": "Control_Control_Control",
            "post_normalization_column_merges": [],
            "generate_qvalue_plots": True,
        },
    }


def main():
    parser = argparse.ArgumentParser(description="Generate project_manifest.yaml from the copied project structure.")
    parser.add_argument("--project-root", default=".", help="Path to the copied notebook_proteomics project root")
    parser.add_argument("--project-id", default="")
    parser.add_argument("--project-title", default="")
    parser.add_argument("--organism", default="")
    parser.add_argument("--material", default="")
    parser.add_argument("--analysis-owner", default="")
    parser.add_argument("--force", action="store_true", help="Overwrite an existing project_manifest.yaml")
    args = parser.parse_args()

    project_root = Path(args.project_root).resolve()
    config_dir = project_root / "workflow" / "00_raw_data" / "config"
    config_dir.mkdir(parents=True, exist_ok=True)
    manifest_path = config_dir / "project_manifest.yaml"
    if manifest_path.exists() and not args.force:
        raise FileExistsError(f"{manifest_path} already exists. Re-run with --force to overwrite it.")

    manifest = infer_manifest(
        project_root,
        project_id=args.project_id,
        project_title=args.project_title,
        organism=args.organism,
        material=args.material,
        analysis_owner=args.analysis_owner,
    )
    with open(manifest_path, "w", encoding="utf-8") as handle:
        handle.write(render_manifest_with_comments(manifest))
    print(f"Wrote {manifest_path}")


if __name__ == "__main__":
    main()
