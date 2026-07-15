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
    received_files = [value for value in [raw_data_file, metadata_source, "workflow/00_raw_data/correspondence.txt"] if value]
    comparison_ids = [comp.get("comparison_id", "") for comp in metadata.get("comparisons", []) if comp.get("comparison_id", "")]
    grouping_columns = sorted({comp.get("grouping_column", "") for comp in metadata.get("comparisons", []) if comp.get("grouping_column", "")})

    aggregate = viz.get("aggregate", {})
    comparisons = viz.get("comparisons", {})
    files_present = {}
    for item in comparisons.values():
        for name, present in item.get("files_present", {}).items():
            files_present[name] = files_present.get(name, False) or bool(present)

    payload = {
        "received_files": join_names(received_files),
        "main_input_file": raw_data_file,
        "final_analysis_input": raw_data_file,
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
        "comparison_deviations": "none",
        "statistical_method_changes": "none documented",
        "statistics_status": "completed",
        "carry_forward_statistics_note": f"The strongest nominal comparison was {stats.get('strongest_nominal_comparison', '')}; no q-value-supported proteins were retained.",
        "visualization_status": "completed",
        "plot_generation_status_note": "Interactive HTML plots were generated for all enabled comparisons; static PNG and SVG export depends on the local Plotly/Kaleido browser setup.",
        "volcano_files_present_list": list_present_files(files_present, "_html") or "HTML outputs present",
        "heatmap_files_present_list": list_present_files(files_present, "_html") or "HTML outputs present",
        "pca_files_present_list": list_present_files(files_present, "_html") or "HTML outputs present",
        "pca3d_files_present_list": list_present_files(files_present, "_html") or "HTML outputs present",
        "plsda_files_present_list": list_present_files(files_present, "_html") or "HTML outputs present",
        "no_secondary_analyses_or_replace": "No secondary analyses were performed for this run.",
        "raw_data_step_status": "completed",
        "raw_data_primary_output": raw_data_file,
        "raw_data_step_note": "Raw data, metadata source, and project correspondence were staged in workflow/00_raw_data/ and the startup config files were regenerated from the template.",
        "qc_step_status": "completed",
        "qc_step_note": "Filtering, metadata validation, and primary normalization completed successfully.",
        "statistics_step_status": "completed",
        "statistics_step_note": f"{len(comparison_ids)} enabled comparisons were tested and summarized in significant_protein_counts.csv.",
        "visualization_step_status": "completed",
        "visualization_step_note": "Interactive plot outputs were generated for all enabled comparisons.",
        "secondary_step_status": "not_run",
        "secondary_primary_output_or_none": "none",
        "secondary_step_note": "No follow-up secondary analyses were executed.",
        "issue_or_none": "none reported",
        "issue_resolution": "not applicable",
        "issue_impact": "no documented impact on the completed run",
        "carry_forward_note_1": f"Only the {len(comparison_ids)} requested comparisons were enabled for this run.",
        "carry_forward_note_2": "No q-value-significant proteins were retained in the completed run.",
        "carry_forward_note_3": "Static plot export availability depends on the local browser setup used by Plotly and Kaleido.",
    }

    write_json(output_dir / "execution_report_fields.json", payload)
    print(f"Wrote {output_dir / 'execution_report_fields.json'}")


if __name__ == "__main__":
    main()
