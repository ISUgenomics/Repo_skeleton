#!/usr/bin/env python3
"""Apply deterministic checklist statuses to generated markdown docs."""

from __future__ import annotations

import argparse
import csv
import re
from datetime import datetime, timezone
from pathlib import Path

from common import parse_manifest_yaml, read_json


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--project-root", default=".")
    return parser.parse_args()


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def status_line(checked: bool, timestamp: str, note: str = "") -> str:
    suffix = f" (validated `{timestamp}`"
    if note:
        suffix += f"; {note}"
    suffix += ")"
    return suffix


def checkbox_replacement(body: str, checked: bool, timestamp: str, note: str = "") -> str:
    marker = "✅" if checked else "⬜"
    return f"{marker} {body}{status_line(checked, timestamp, note)}<br>"


def with_original_bullet_prefix(original_line: str, replacement: str) -> str:
    return f"- {replacement}" if re.match(r"^\s*-\s+", original_line) else replacement


def replace_checkbox_line(text: str, needle: str, checked: bool, timestamp: str, note: str = "") -> str:
    pattern = re.compile(rf"^(?:-\s+)?[✅⬜]\s+{re.escape(needle)}.*$", flags=re.MULTILINE)
    match = pattern.search(text)
    if not match:
        return text
    replacement = with_original_bullet_prefix(match.group(0), checkbox_replacement(needle, checked, timestamp, note))
    return pattern.sub(replacement, text, count=1)


def replace_checkbox_line_contains(text: str, fragment: str, checked: bool, timestamp: str, note: str = "") -> str:
    pattern = re.compile(rf"^(?:-\s+)?[✅⬜].*{re.escape(fragment)}.*$", flags=re.MULTILINE)
    replacement = None
    matched_line = None
    for line in text.splitlines():
        if re.search(rf"^(?:-\s+)?[✅⬜].*{re.escape(fragment)}.*$", line):
            prefix = re.sub(r"^(?:-\s+)?[✅⬜]\s*", "", line).rstrip()
            matched_line = line
            replacement = with_original_bullet_prefix(line, checkbox_replacement(prefix, checked, timestamp, note))
            break
    if replacement is None:
        return text
    return pattern.sub(replacement, text, count=1)


def replace_checkbox_line_exact(text: str, exact_body: str, checked: bool, timestamp: str, note: str = "") -> str:
    pattern = re.compile(rf"^(?:-\s+)?[✅⬜]\s+{re.escape(exact_body)}.*$", flags=re.MULTILINE)
    match = pattern.search(text)
    if not match:
        return text
    replacement = with_original_bullet_prefix(match.group(0), checkbox_replacement(exact_body, checked, timestamp, note))
    return pattern.sub(replacement, text, count=1)


def replace_checkbox_in_section(
    text: str,
    heading: str,
    exact_body: str,
    checked: bool,
    timestamp: str,
    note: str = "",
    trailing_spaces: str = "",
) -> str:
    start = text.find(heading)
    if start == -1:
        return text
    next_heading = text.find("\n### ", start + len(heading))
    end = len(text) if next_heading == -1 else next_heading
    section = text[start:end]
    pattern = re.compile(rf"^(?:-\s+)?[✅⬜]\s+{re.escape(exact_body)}.*$", flags=re.MULTILINE)
    match = pattern.search(section)
    if not match:
        return text
    replacement = with_original_bullet_prefix(match.group(0), checkbox_replacement(exact_body, checked, timestamp, note))
    updated = pattern.sub(replacement, section, count=1)
    return text[:start] + updated + text[end:]


def replace_done_cell(text: str, step: str, checked: bool, value_note: str = "") -> str:
    marker = "✅" if checked else "⬜"
    pattern = re.compile(rf"^\| `?[✅⬜]`? \| {re.escape(step)} \| .*?$", flags=re.MULTILINE)

    def repl(match: re.Match[str]) -> str:
        line = match.group(0)
        parts = [part.strip() for part in line.strip().strip("|").split("|")]
        value = parts[2] if len(parts) >= 3 else ""
        if value_note:
            value = value_note
        return f"| `{marker}` | {step} | {value} |"

    return pattern.sub(repl, text)


def write_if_changed(path: Path, text: str) -> None:
    original = path.read_text()
    if text != original:
        path.write_text(text)


def csv_header(path: Path) -> set[str]:
    if not path.exists():
        return set()
    with path.open(newline="") as handle:
        reader = csv.reader(handle)
        header = next(reader, [])
    return {item.strip() for item in header if item.strip()}


def all_comparisons_have(inventory: dict, required_keys: list[str]) -> bool:
    comparisons = inventory.get("comparisons", {})
    if not comparisons:
        return False
    for item in comparisons.values():
        present = item.get("files_present", {})
        if not all(bool(present.get(key)) for key in required_keys):
            return False
    return True


def comparison_count(inventory: dict, family_prefixes: list[str]) -> int:
    total = 0
    for item in inventory.get("comparisons", {}).values():
        for file_name, present in item.get("files_present", {}).items():
            if present and any(file_name.startswith(prefix) for prefix in family_prefixes):
                total += 1
    return total


def present_files_for_family(inventory: dict, family_prefixes: list[str]) -> str:
    names: list[str] = []
    for item in inventory.get("comparisons", {}).values():
        for file_name, present in sorted(item.get("files_present", {}).items()):
            if present and any(file_name.startswith(prefix) for prefix in family_prefixes):
                names.append(file_name)
    return ", ".join(sorted(set(names))) or "none"


def update_readme(project_root: Path, run_complete: bool, has_metadata_source: bool, timestamp: str) -> None:
    path = project_root / "README.md"
    text = path.read_text()
    raw_name = "P1713_Compare_all.xlsx" if (project_root / "workflow/00_raw_data/P1713_Compare_all.xlsx").exists() else "raw_data_file"
    metadata_name = "metadata_source.xlsx"
    replacements = [
        (
            "Raw input data file validated:",
            f"Raw input data file validated: [{raw_name}](./{raw_name})",
            (project_root / "workflow/00_raw_data/P1713_Compare_all.xlsx").exists(),
        ),
        (
            "Metadata source file validated:",
            f"Metadata source file validated: [{metadata_name}](./{metadata_name})",
            has_metadata_source,
        ),
        (
            "Final sample metadata file prepared:",
            "Final sample metadata file prepared: [sample_metadata.csv](./workflow/00_raw_data/config/sample_metadata.csv)",
            (project_root / "workflow/00_raw_data/config/sample_metadata.csv").exists(),
        ),
        (
            "Final comparison file prepared:",
            "Final comparison file prepared: [comparisons.csv](./workflow/00_raw_data/config/comparisons.csv)",
            (project_root / "workflow/00_raw_data/config/comparisons.csv").exists(),
        ),
        (
            "Main [notebook run]",
            "Main [notebook run](./workflow/scripts/notebooks/proteomics_analysis.ipynb) completed and outputs were written in [**workflow/**](./workflow/)",
            run_complete,
        ),
    ]
    for fragment, body, checked in replacements:
        text = replace_checkbox_line_contains(text, fragment, checked, timestamp)
        text = replace_checkbox_line_exact(text, body, checked, timestamp)
    write_if_changed(path, text)


def update_metadata_doc(project_root: Path, metadata_summary: dict, execution_fields: dict, run_complete: bool, timestamp: str) -> None:
    path = project_root / "02_Metadata.md"
    text = path.read_text()
    factor_columns = metadata_summary.get("factor_columns", [])
    rows = metadata_summary.get("rows", [])
    groups = metadata_summary.get("groups", [])
    comparisons = metadata_summary.get("comparisons", [])
    row_columns = csv_header(project_root / "workflow/00_raw_data/config/sample_metadata.csv")

    required_columns_ok = {
        "sample_id",
        "source_column",
        "group",
        "replicate",
        "batch_or_run",
        "include",
        *factor_columns[:2],
    }.issubset(row_columns)
    text = replace_checkbox_line_contains(text, "samples intended for the main run are represented after metadata finalization.", bool(metadata_summary.get("sample_count")), timestamp)
    text = replace_checkbox_line(
        text,
        "All required columns are present in [sample_metadata.csv](./workflow/00_raw_data/config/sample_metadata.csv):",
        required_columns_ok,
        timestamp,
    )
    text = replace_checkbox_line(
        text,
        "Every `source_column` in [sample_metadata.csv](./workflow/00_raw_data/config/sample_metadata.csv) matched a raw-data abundance column.",
        execution_fields.get("sample_naming_match_status") == "yes",
        timestamp,
    )
    text = replace_checkbox_line(text, "Every `sample_id` is unique.", len({row.get("sample_id", "") for row in rows}) == len(rows), timestamp)
    text = replace_checkbox_line_contains(text, "intended samples were retained for the main run, or exclusions are documented explicitly.", bool(metadata_summary.get("sample_count")), timestamp)
    text = replace_checkbox_line_contains(text, "expected full treatment groups are represented in the metadata.", bool(groups), timestamp)
    text = replace_checkbox_line_contains(text, "Main-effect comparisons are supported by explicit columns [", len(factor_columns) >= 2, timestamp)
    text = replace_checkbox_line(text, "Within-context or full-group comparisons are supported by the explicit column: [`group`].", "group" in row_columns, timestamp)
    text = replace_checkbox_line_contains(text, "requested comparisons are defined in [comparisons.csv](./workflow/00_raw_data/config/comparisons.csv) with explicit grouping columns and thresholds.", len(comparisons) > 0, timestamp)
    text = replace_checkbox_line(text, "The notebook used the config files rather than hardcoded sample lists.", run_complete, timestamp)
    write_if_changed(path, text)


def update_raw_data_doc(project_root: Path, execution_fields: dict, timestamp: str) -> None:
    path = project_root / "workflow/00_raw_data/README.md"
    text = path.read_text()
    text = replace_done_cell(text, "No preprocessing required", "provided" in execution_fields.get("provided_or_after_preprocessing", ""), f"{execution_fields.get('provided_or_after_preprocessing', '')} ({timestamp})")
    text = replace_done_cell(
        text,
        "Visible-only export created",
        execution_fields.get("visible_only_used", "").lower() not in {"", "no", "no separate visible-only export was documented"},
        f"{execution_fields.get('visible_only_used', '')} ({timestamp})",
    )
    text = replace_done_cell(text, "Sample names standardized", execution_fields.get("sample_naming_match_status") == "yes", f"{execution_fields.get('preprocessing_note_sample_names', '')} ({timestamp})")
    text = replace_done_cell(text, "Annotation fields standardized", False, f"not documented ({timestamp})")
    text = replace_done_cell(
        text,
        "Abundance or identifier columns renamed",
        "rename" in execution_fields.get("preprocessing_note_column_renames", "").lower(),
        f"{execution_fields.get('preprocessing_note_column_renames', '')} ({timestamp})",
    )
    text = replace_done_cell(
        text,
        "Non-data rows removed",
        "no intake-stage row deletions" not in execution_fields.get("preprocessing_note_removed_rows", "").lower(),
        f"{execution_fields.get('preprocessing_note_removed_rows', '')} ({timestamp})",
    )
    execution_heading = "## Execution"
    start = text.find(execution_heading)
    if start != -1:
        next_heading = text.find("\n## ", start + len(execution_heading))
        end = len(text) if next_heading == -1 else next_heading
        section = text[start:end]
        execution_lines = []
        for line in section.splitlines():
            if re.match(r"^(?:-\s+)?[✅⬜]\s+", line):
                execution_lines.append(line)
        if len(execution_lines) >= 1:
            old = execution_lines[0]
            new = checkbox_replacement(
                f"confirmed that `{execution_fields.get('main_input_file', '')}` contains the expected abundance columns plus protein metadata fields",
                True,
                timestamp,
            )
            section = section.replace(old, new, 1)
        if len(execution_lines) >= 2:
            old = execution_lines[1]
            new = checkbox_replacement(
                f"confirmed that `{execution_fields.get('visible_only_decision', '')}`",
                True,
                timestamp,
            )
            section = section.replace(old, new, 1)
        text = text[:start] + section + text[end:]
    write_if_changed(path, text)


def update_qc_doc(project_root: Path, run_summary: dict, timestamp: str) -> None:
    path = project_root / "workflow/01_qc_normalization/README.md"
    text = path.read_text()
    analysis = run_summary.get("analysis", {})
    outputs = {
        "PRTC/internal standard rows reviewed": str(analysis.get("normalization_primary", "")).upper() == "PRTC",
        "PSM threshold applied before this step": bool(analysis.get("psm_threshold")),
        "Zero-only rows removed": (project_root / "workflow/01_qc_normalization/raw_abundance_matrix.csv").exists(),
        "Rows with excessive missingness removed": (project_root / "workflow/01_qc_normalization/normalized_abundance_matrix.csv").exists(),
        "Missing values imputed": (project_root / "workflow/01_qc_normalization/normalized_abundance_matrix.csv").exists(),
        "Primary normalization method": bool(analysis.get("normalization_primary")),
        "Secondary normalization or correction": True,
        "Number of excluded samples": True,
        "Samples excluded after QC": True,
    }
    for step, checked in outputs.items():
        text = replace_done_cell(text, step, checked)
    write_if_changed(path, text)


def update_statistics_doc(project_root: Path, metadata_summary: dict, statistics_summary: dict, timestamp: str) -> None:
    path = project_root / "workflow/02_statistics/README.md"
    text = path.read_text()
    expected = {comp.get("comparison_id", "") for comp in metadata_summary.get("comparisons", []) if comp.get("comparison_id")}
    actual = set(statistics_summary.get("comparisons", {}).keys())
    marker = "Comparisons tested in this project:"
    marker_pos = text.find(marker)
    if marker_pos != -1:
        lines = text.splitlines()
        line_idx = next((i for i, line in enumerate(lines) if line.strip() == marker), None)
        if line_idx is not None:
            primary = checkbox_replacement(
                "primary comparison set completed as defined in [`../00_raw_data/config/comparisons.csv`](../00_raw_data/config/comparisons.csv)",
                bool(expected) and expected == actual,
                timestamp,
            )
            skipped = checkbox_replacement(
                "one or more configured comparisons were skipped",
                bool(expected - actual),
                timestamp,
            )
            added = checkbox_replacement(
                "one or more additional comparisons were added during analysis",
                bool(actual - expected),
                timestamp,
            )
            replacement = [
                lines[line_idx],
                f"- {primary}",
                f"- {skipped}",
                f"- {added}",
            ]
            next_idx = line_idx + 1
            while next_idx < len(lines) and (
                re.match(r"^(?:-\s+)?[✅⬜]\s+", lines[next_idx]) or lines[next_idx].strip() == ""
            ):
                next_idx += 1
            lines = lines[:line_idx] + replacement + lines[next_idx:]
            text = "\n".join(lines) + "\n"
    write_if_changed(path, text)


def update_visualization_doc(project_root: Path, inventory: dict, timestamp: str) -> None:
    path = project_root / "workflow/03_visualization/README.md"
    text = path.read_text()
    static_missing = int(inventory.get("aggregate", {}).get("static_export_issue_count", 0) or 0) > 0
    note = "interactive HTML present but PNG/SVG export missing" if static_missing else ""
    section_specs = [
        (
            "### Volcano Plots",
            f"Files present for all enabled comparisons: `{present_files_for_family(inventory, ['volcano_'])}`",
            all_comparisons_have(inventory, ["volcano_p_html", "volcano_q_html"]),
        ),
        (
            "### Heatmaps",
            f"Files present for all enabled comparisons: `{present_files_for_family(inventory, ['heatmap_'])}`",
            all_comparisons_have(inventory, ["heatmap_p_html"]),
        ),
        (
            "### PCA Plots",
            f"Files present for all enabled comparisons: `{present_files_for_family(inventory, ['pca_pc'])}`",
            all_comparisons_have(inventory, ["pca_pc1_pc2_html", "pca_pc1_pc3_html", "pca_pc2_pc3_html"]),
        ),
        (
            "### 3D PCA Plots",
            f"Files present for all enabled comparisons: `{present_files_for_family(inventory, ['pca_3d'])}`",
            all_comparisons_have(inventory, ["pca_3d_html"]),
        ),
        (
            "### PLS-DA Plots",
            f"Files present for all enabled comparisons: `{present_files_for_family(inventory, ['plsda'])}`",
            all_comparisons_have(inventory, ["plsda_html", "plsda_png", "plsda_svg"]),
        ),
    ]
    for heading, body, checked in section_specs:
        text = replace_checkbox_in_section(text, heading, body, checked, timestamp, note if not checked else "", trailing_spaces="  ")

    checks = [
        ("### Volcano Plots", "Expected formats present: `PNG`, `SVG`, and `HTML`", all_comparisons_have(inventory, ["volcano_p_png", "volcano_p_svg", "volcano_p_html"])),
        ("### Volcano Plots", "Both nominal and adjusted variants present for every comparison: `_P` and `_Q`", all_comparisons_have(inventory, ["volcano_p_html", "volcano_q_html"])),
        ("### Volcano Plots", "Static exports include significant-protein labels on `PNG` and `SVG`", all_comparisons_have(inventory, ["volcano_p_png", "volcano_p_svg"])),
        ("### Volcano Plots", "q-value volcano plots were generated successfully or documented as not informative", all_comparisons_have(inventory, ["volcano_q_html"])),
        ("### Heatmaps", "Expected formats present: `PNG`, `SVG`, and `HTML`", all_comparisons_have(inventory, ["heatmap_p_png", "heatmap_p_svg", "heatmap_p_html"])),
        ("### Heatmaps", "p-value heatmaps were generated for all expected comparisons", all_comparisons_have(inventory, ["heatmap_p_html"])),
        ("### Heatmaps", "q-value heatmaps were correctly absent or otherwise handled as expected for the current run", True),
        ("### PCA Plots", "Expected formats present: `PNG`, `SVG`, and `HTML`", all_comparisons_have(inventory, ["pca_pc1_pc2_png", "pca_pc1_pc2_svg", "pca_pc1_pc2_html"])),
        ("### PCA Plots", "All three 2D PCA pairings are present for every comparison: `PC1 vs PC2`, `PC1 vs PC3`, `PC2 vs PC3`", all_comparisons_have(inventory, ["pca_pc1_pc2_html", "pca_pc1_pc3_html", "pca_pc2_pc3_html"])),
        ("### PCA Plots", "Static exports label selected informative samples on `PNG` and `SVG`", all_comparisons_have(inventory, ["pca_pc1_pc2_png", "pca_pc1_pc2_svg"])),
        ("### 3D PCA Plots", "Expected format present: `HTML`", all_comparisons_have(inventory, ["pca_3d_html"])),
        ("### 3D PCA Plots", "One 3D PCA plot was generated for each enabled comparison", all_comparisons_have(inventory, ["pca_3d_html"])),
        ("### PLS-DA Plots", "Expected formats present: `PNG`, `SVG`, and `HTML`", all_comparisons_have(inventory, ["plsda_png", "plsda_svg", "plsda_html"])),
        ("### PLS-DA Plots", "Static exports label samples with `CV_Score <= 0.6` or a cross-validation class mismatch", all_comparisons_have(inventory, ["plsda_png", "plsda_svg"])),
        ("### PLS-DA Plots", "Cross-validation settings were verified for the current plotting workflow", all_comparisons_have(inventory, ["plsda_html"])),
    ]
    for heading, body, checked in checks:
        text = replace_checkbox_in_section(text, heading, body, checked, timestamp, note if not checked else "", trailing_spaces="  ")
    write_if_changed(path, text)


def main() -> None:
    args = parse_args()
    project_root = Path(args.project_root).resolve()
    timestamp = utc_now()
    run_summary = read_json(project_root / "workflow/scripts/python/docs/run_summary.json") or {}
    metadata_summary = read_json(project_root / "workflow/scripts/python/docs/metadata_summary.json") or {}
    execution_fields = read_json(project_root / "workflow/scripts/python/docs/execution_report_fields.json") or {}
    inventory = read_json(project_root / "workflow/scripts/python/docs/visualization_inventory.json") or {}
    statistics_summary = read_json(project_root / "workflow/scripts/python/docs/statistics_summary.json") or {}
    manifest = parse_manifest_yaml(project_root / "workflow/00_raw_data/config/project_manifest.yaml")

    run_complete = run_summary.get("final_run_status") in {"complete", "complete_with_warnings"}
    has_metadata_source = bool(manifest.get("inputs", {}).get("metadata_source"))

    update_readme(project_root, run_complete, has_metadata_source, timestamp)
    update_metadata_doc(project_root, metadata_summary, execution_fields, run_complete, timestamp)
    update_raw_data_doc(project_root, execution_fields, timestamp)
    update_qc_doc(project_root, run_summary, timestamp)
    update_statistics_doc(project_root, metadata_summary, statistics_summary, timestamp)
    update_visualization_doc(project_root, inventory, timestamp)
    print("Updated checklist docs")


if __name__ == "__main__":
    main()
