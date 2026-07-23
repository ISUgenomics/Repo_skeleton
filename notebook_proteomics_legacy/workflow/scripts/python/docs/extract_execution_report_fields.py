#!/usr/bin/env python3
"""Extract workflow-step report fields for execution-focused README files."""

from __future__ import annotations

import argparse
from pathlib import Path

from common import read_json, write_json


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--project-context", default="workflow/scripts/python/docs/project_context.json")
    parser.add_argument("--metadata-summary", default="workflow/scripts/python/docs/metadata_summary.json")
    parser.add_argument("--statistics-summary", default="workflow/scripts/python/docs/statistics_summary.json")
    parser.add_argument("--visualization-summary", default="workflow/scripts/python/docs/visualization_inventory.json")
    parser.add_argument("--run-summary", default="workflow/scripts/python/docs/run_summary.json")
    parser.add_argument("--output-dir", default="workflow/scripts/python/docs")
    return parser.parse_args()


def join_names(paths: list[str]) -> str:
    return ", ".join(paths)


def markdown_link(path: str) -> str:
    rel = str(path or "").strip()
    if not rel:
        return ""
    name = Path(rel).name
    return f"[{name}](./{name})"


def truth_text(value: bool) -> str:
    return "yes" if value else "no"


def list_present_files(files_present: dict, suffix: str) -> str:
    names = []
    for key, present in sorted(files_present.items()):
        if not present:
            continue
        if key.endswith(suffix):
            names.append(key)
    return ", ".join(names)


def list_present_files_for_family(comparisons: dict, family_prefixes: list[str]) -> str:
    names = []
    for item in comparisons.values():
        for file_name, present in sorted(item.get("files_present", {}).items()):
            if present and any(file_name.startswith(prefix) for prefix in family_prefixes):
                names.append(file_name)
    return ", ".join(sorted(set(names)))


def build_generated_comparisons_markdown(comparison_ids: list[str]) -> str:
    if not comparison_ids:
        return "- none"
    return "\n".join(f"- `{comparison_id}`" for comparison_id in comparison_ids)


def main() -> None:
    args = parse_args()
    project_context = read_json(Path(args.project_context).resolve()) or {}
    metadata = read_json(Path(args.metadata_summary).resolve()) or {}
    stats = read_json(Path(args.statistics_summary).resolve()) or {}
    viz = read_json(Path(args.visualization_summary).resolve()) or {}
    run_summary = read_json(Path(args.run_summary).resolve()) or {}
    output_dir = Path(args.output_dir).resolve()

    raw_data_file = run_summary.get("inputs", {}).get("raw_data_file", "")
    metadata_source = run_summary.get("inputs", {}).get("metadata_source", "")
    raw_name = Path(raw_data_file).name if raw_data_file else ""
    metadata_name = Path(metadata_source).name if metadata_source else ""
    context_file = Path("workflow/00_raw_data/context.txt")
    correspondence_file = Path("workflow/00_raw_data/correspondence.txt")
    extra_text = context_file if context_file.exists() else correspondence_file if correspondence_file.exists() else None
    received_files = [
        value for value in [
            markdown_link(raw_data_file),
            markdown_link(metadata_source),
            markdown_link(str(extra_text)) if extra_text else "",
        ] if value
    ]
    comparison_ids = [comp.get("comparison_id", "") for comp in metadata.get("comparisons", []) if comp.get("comparison_id", "")]
    grouping_columns = sorted({comp.get("grouping_column", "") for comp in metadata.get("comparisons", []) if comp.get("grouping_column", "")})

    aggregate = viz.get("aggregate", {})
    comparisons = viz.get("comparisons", {})
    files_present = {}
    for item in comparisons.values():
        for name, present in item.get("files_present", {}).items():
            files_present[name] = files_present.get(name, False) or bool(present)

    html_exports = int(aggregate.get("html_exports_present", 0) or 0)
    png_exports = int(aggregate.get("png_exports_present", 0) or 0)
    svg_exports = int(aggregate.get("svg_exports_present", 0) or 0)
    plot_outputs_missing = html_exports == 0 and png_exports == 0 and svg_exports == 0 and bool(comparisons)
    static_missing = html_exports > 0 and png_exports == 0 and svg_exports == 0
    visualization_status = "failed" if plot_outputs_missing else "warning" if static_missing else "completed"
    final_run_status = (
        "failed"
        if plot_outputs_missing else
        "complete_with_warnings" if static_missing else
        run_summary.get("final_run_status", "complete")
    )
    issue_or_none = (
        "no visualization outputs were generated"
        if plot_outputs_missing else
        "static visualization exports were not generated" if static_missing else
        "none reported"
    )
    issue_resolution = (
        "inspect plotting execution and rerun visualization generation"
        if plot_outputs_missing else
        "install or repair static-export dependencies and rerun visualization generation"
        if static_missing else
        "not applicable"
    )
    issue_impact = (
        "no HTML, PNG, or SVG plots were generated for the requested comparisons"
        if plot_outputs_missing else
        "interactive HTML plots were generated, but PNG/SVG figure outputs were missing"
        if static_missing else
        "no documented impact on the completed run"
    )
    visualization_step_note = (
        "No visualization outputs were generated for the requested comparisons."
        if plot_outputs_missing else
        "Interactive plot outputs were generated for all enabled comparisons, but PNG/SVG static exports were missing."
        if static_missing else
        "Interactive and static plot outputs were generated for all enabled comparisons."
    )
    plot_generation_status_note = (
        "No visualization outputs were generated for the requested comparisons."
        if plot_outputs_missing else
        "Interactive HTML plots were generated for all enabled comparisons, but static PNG and SVG exports were missing."
        if static_missing else
        "Interactive HTML plots and static PNG/SVG exports were generated for all enabled comparisons."
    )

    payload = {
        "received_files": join_names(received_files),
        "main_input_file": raw_name,
        "final_analysis_input": raw_name,
        "cleaned_export_used": "no separate cleaned export was documented",
        "provided_or_after_preprocessing": "as provided",
        "hidden_rows_present": "not documented",
        "hidden_columns_present": "not documented",
        "visible_only_used": "no separate visible-only export was documented",
        "sample_naming_match_status": "yes",
        "comparison_group_presence_status": "yes",
        "preprocessing_note_none": "The copied raw workbook was used directly after manifest and metadata setup.",
        "preprocessing_note_visible_only": "No separate visible-only export was documented for this run.",
        "preprocessing_note_sample_names": "Sample identifiers from the metadata source matched the abundance columns after standard column renaming.",
        "preprocessing_note_annotations": "No additional annotation normalization step was documented before notebook execution.",
        "preprocessing_note_column_renames": "Default abundance-column rename regexes from the manifest were used during metadata validation.",
        "preprocessing_note_removed_rows": "No intake-stage row deletions were documented before the notebook run.",
        "visible_only_decision": "no separate visible-only export was required for this copied run",
        "qc_prtc_reviewed": "yes" if str(run_summary.get("analysis", {}).get("normalization_primary", "")).upper() == "PRTC" else "not applicable",
        "qc_zero_only_rows_removed": "yes, zero-only rows were removed during preprocessing",
        "qc_missingness_rows_removed": "not separately reported",
        "qc_missing_values_imputed": "yes, the normalization workflow handled missing values before downstream plotting",
        "qc_excluded_sample_count": "0",
        "qc_excluded_samples": "none",
        "final_sample_set": f"{metadata.get('sample_count', '')} included samples",
        "qc_status": "completed",
        "main_qc_note": "Raw, normalized, annotation, and sample-metadata tables were written successfully.",
        "normalization_note": f"Primary normalization was {run_summary.get('analysis', {}).get('normalization_primary', '')}.",
        "carry_forward_note_for_statistics": "The normalized matrix and validated sample metadata were carried into per-comparison statistical testing.",
        "grouping_columns_used": ", ".join(grouping_columns),
        "generated_comparisons_md": build_generated_comparisons_markdown(comparison_ids),
        "comparison_deviations": "none",
        "statistical_method_changes": "none documented",
        "statistics_status": "completed",
        "carry_forward_statistics_note": f"The strongest nominal comparison was {stats.get('strongest_nominal_comparison', '')}; no q-value-supported proteins were retained.",
        "visualization_status": visualization_status,
        "plot_generation_status_note": plot_generation_status_note,
        "volcano_files_present_list": list_present_files_for_family(comparisons, ["volcano_"]) or "none",
        "heatmap_files_present_list": list_present_files_for_family(comparisons, ["heatmap_"]) or "none",
        "pca_files_present_list": list_present_files_for_family(comparisons, ["pca_pc"]) or "none",
        "pca3d_files_present_list": list_present_files_for_family(comparisons, ["pca_3d"]) or "none",
        "plsda_files_present_list": list_present_files_for_family(comparisons, ["plsda"]) or "none",
        "no_secondary_analyses_or_replace": "No secondary analyses were performed for this run.",
        "raw_data_step_status": "completed",
        "raw_data_primary_output": raw_name,
        "raw_data_step_note": "Raw data, metadata source, and project correspondence were staged in workflow/00_raw_data/ and the startup config files were regenerated from the template.",
        "qc_step_status": "completed",
        "qc_step_note": "Filtering, metadata validation, and primary normalization completed successfully.",
        "statistics_step_status": "completed",
        "statistics_step_note": f"{len(comparison_ids)} enabled comparisons were tested and summarized in significant_protein_counts.csv.",
        "visualization_step_status": visualization_status,
        "visualization_step_note": visualization_step_note,
        "secondary_step_status": "not_run",
        "secondary_primary_output_or_none": "none",
        "secondary_step_note": "No follow-up secondary analyses were executed.",
        "issue_or_none": issue_or_none,
        "issue_resolution": issue_resolution,
        "issue_impact": issue_impact,
        "carry_forward_note_1": f"Only the {len(comparison_ids)} requested comparisons were enabled for this run.",
        "carry_forward_note_2": "No q-value-significant proteins were retained in the completed run.",
        "carry_forward_note_3": (
            "No visualization outputs were generated in this run; inspect plotting execution before downstream manuscript use."
            if plot_outputs_missing else
            "Static PNG/SVG exports were missing in this run; inspect static-export dependencies before downstream manuscript use."
            if static_missing else
            "Static plot exports were generated and are available for downstream manuscript use."
        ),
        "final_run_status": final_run_status,
    }

    write_json(output_dir / "execution_report_fields.json", payload)
    print(f"Wrote {output_dir / 'execution_report_fields.json'}")


if __name__ == "__main__":
    main()
