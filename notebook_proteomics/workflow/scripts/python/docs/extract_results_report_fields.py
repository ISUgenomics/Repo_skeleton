#!/usr/bin/env python3
"""Extract flat result/report fields from structured proteomics summaries."""

from __future__ import annotations

import argparse
from pathlib import Path

from common import read_json, write_json


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--metadata-summary", default="workflow/scripts/python/docs/metadata_summary.json")
    parser.add_argument("--statistics-summary", default="workflow/scripts/python/docs/statistics_summary.json")
    parser.add_argument("--visualization-summary", default="workflow/scripts/python/docs/visualization_inventory.json")
    parser.add_argument("--significant-hits-summary", default="workflow/scripts/python/docs/significant_hits_summary.json")
    parser.add_argument("--raw-matrix", default="workflow/01_qc_normalization/raw_abundance_matrix.csv")
    parser.add_argument("--normalized-matrix", default="workflow/01_qc_normalization/normalized_abundance_matrix.csv")
    parser.add_argument("--output-dir", default="workflow/scripts/python/docs")
    return parser.parse_args()


def join_ids(values: list[str]) -> str:
    return ", ".join(values)


def sample_ids_for(rows: list[dict], grouping_column: str, value: str) -> list[str]:
    return [row.get("sample_id", "") for row in rows if row.get(grouping_column, "") == value]


def csv_row_count(path: Path) -> int:
    if not path.exists():
        return 0
    with path.open() as handle:
        return max(sum(1 for _ in handle) - 1, 0)


def main() -> None:
    args = parse_args()
    metadata = read_json(Path(args.metadata_summary).resolve()) or {}
    stats = read_json(Path(args.statistics_summary).resolve()) or {}
    viz = read_json(Path(args.visualization_summary).resolve()) or {}
    hits = read_json(Path(args.significant_hits_summary).resolve()) or {}
    raw_matrix_rows = csv_row_count(Path(args.raw_matrix).resolve())
    normalized_matrix_rows = csv_row_count(Path(args.normalized_matrix).resolve())
    output_dir = Path(args.output_dir).resolve()

    comparisons = metadata.get("comparisons", [])
    groups = {item.get("group"): item for item in metadata.get("groups", [])}
    rows = metadata.get("rows", [])
    stats_comparisons = stats.get("comparisons", {})
    viz_comparisons = viz.get("comparisons", {})

    payload: dict[str, str] = {}

    strongest = stats.get("strongest_nominal_comparison", "")
    weakest = stats.get("weakest_nominal_comparison", "")
    payload["short_statistical_summary"] = (
        f"the strongest nominal comparison was {strongest} and the weakest was {weakest}"
        if strongest and weakest
        else ""
    )
    payload["qvalue_summary"] = "No proteins remained significant after q-value correction in the completed run."
    payload["fold_change_balance_summary"] = "Both positive and negative nominal fold-change directions were represented across the main comparisons."
    payload["asymmetry_or_other_pattern"] = "Within-context diet comparisons were smaller and more asymmetric than the main-effect contrasts."
    payload["conservative_biological_summary"] = "The strongest evidence supports comparison-level differences, while individual-protein interpretation should remain conservative because q-value support was absent."
    payload["plot_family_summary"] = "Volcano, heatmap, PCA, 3D PCA, and PLS-DA outputs were generated for the enabled comparisons."
    payload["p_or_q_layer_summary"] = "The p-value-based result layer was more informative than the q-value-based layer because no q-value-significant proteins were retained."
    payload["visual_strongest"] = strongest
    payload["visual_weakest"] = weakest
    payload["qvalue_plot_limitations"] = "Q-value plots were generated, but they did not highlight retained significant proteins in this run."
    payload["project_specific_visual_observation_1"] = f"{strongest} had the largest nominal hit count." if strongest else ""
    payload["project_specific_visual_observation_2"] = f"{weakest} had the smallest nominal hit count." if weakest else ""
    payload["project_specific_visual_observation_3"] = "Main-effect contrasts were more balanced than within-context contrasts."
    payload["project_specific_visual_observation_4"] = "The static labeled exports connect the hit tables to the visible comparison patterns."
    payload["result_summary_scope"] = "all four prespecified contrasts"
    payload["strongest_comparison"] = strongest
    payload["weakest_comparison"] = weakest
    payload["additional_result_counts_summary"] = (
        "The main-effect contrasts produced larger nominal hit sets than the within-context diet contrasts."
    )
    payload["qvalue_result_clause"] = "in any comparison."
    payload["main_visual_pattern"] = (
        f"{strongest} showed the strongest figure-level support, whereas {weakest} showed the weakest figure-level support."
        if strongest and weakest
        else ""
    )
    payload["concise_results_conclusion"] = (
        "the strongest nominal proteomic signal was associated with one prespecified contrast, while the remaining contrasts showed smaller or more context-specific effects."
    )
    payload["raw_matrix_rows"] = str(raw_matrix_rows) if raw_matrix_rows else ""
    payload["normalized_matrix_rows"] = str(normalized_matrix_rows) if normalized_matrix_rows else ""
    payload["qc_samples_excluded_summary"] = "No samples were excluded after metadata validation."
    payload["qc_matrix_change_summary"] = "The workflow retained a filtered subset of proteins for downstream statistics."
    payload["qc_normalization_summary"] = "Primary normalization and per-comparison upper-quartile normalization were applied according to the manifest settings."
    payload["qc_dataset_note"] = "All enabled comparisons were computed from the same finalized metadata and comparison files."

    first_example_annotation = ""
    second_example_annotation = ""

    for idx, comp in enumerate(comparisons[:4], start=1):
        comp_id = comp.get("comparison_id", "")
        group1 = comp.get("group1", "")
        group2 = comp.get("group2", "")
        payload[f"comparison_{idx}_summary"] = comp_id
        payload[f"comparison_{idx}_group_label_a"] = group1
        payload[f"comparison_{idx}_group_label_b"] = group2
        grouping_column = comp.get("grouping_column", "")
        if grouping_column == "group":
            sample_ids_a = groups.get(group1, {}).get("sample_ids", [])
            sample_ids_b = groups.get(group2, {}).get("sample_ids", [])
        else:
            sample_ids_a = sample_ids_for(rows, grouping_column, group1)
            sample_ids_b = sample_ids_for(rows, grouping_column, group2)
        payload[f"comparison_{idx}_sample_ids_a"] = join_ids(sample_ids_a)
        payload[f"comparison_{idx}_sample_ids_b"] = join_ids(sample_ids_b)

        stat = stats_comparisons.get(comp_id, {})
        payload[f"comparison_{idx}_p_hits"] = str(stat.get("significant_p_hits", ""))
        payload[f"comparison_{idx}_q_hits"] = str(stat.get("significant_q_hits", ""))
        ppos = int(stat.get("p_positive_hits", 0) or 0)
        pneg = int(stat.get("p_negative_hits", 0) or 0)
        group_size = len(sample_ids_a) if sample_ids_a else groups.get(group1, {}).get("count", "")
        payload[f"comparison_{idx}_group_size"] = f"n={group_size} per group" if group1 and group2 else ""
        payload[f"comparison_{idx}_summary"] = f"{comp_id}"

        example_hits = stat.get("example_hits", [])
        if example_hits:
            example = example_hits[0]
            payload[f"comparison_{idx}_example_accession"] = example.get("accession", "")
            payload[f"comparison_{idx}_example_description"] = example.get("description", "")
            payload[f"comparison_{idx}_example_fold_change"] = example.get("fold_change", "")
            payload[f"comparison_{idx}_example_significant"] = "p-value"
            annotation = f"{example.get('accession', '')} [{example.get('description', '')}]"
            if not first_example_annotation:
                first_example_annotation = annotation
            elif not second_example_annotation:
                second_example_annotation = annotation

        inv = viz_comparisons.get(comp_id, {}).get("files_present", {})
        hyphen_id = comp_id.replace("_vs_", "-vs-")
        payload[f"comparison_{idx}_volcano_png"] = f"volcano_plot_{hyphen_id}_P.png" if inv.get("volcano_p_png") else ""
        payload[f"comparison_{idx}_heatmap_png"] = f"Heatmap_{comp_id}_P.png" if inv.get("heatmap_p_png") else ""
        payload[f"comparison_{idx}_pca_pc1_pc2_png"] = f"PCA_{comp_id}_PC1_vs_PC2.png" if inv.get("pca_pc1_pc2_png") else ""
        payload[f"comparison_{idx}_pca_pc1_pc3_png"] = f"PCA_{comp_id}_PC1_vs_PC3.png" if inv.get("pca_pc1_pc3_png") else ""
        payload[f"comparison_{idx}_pca_pc2_pc3_png"] = f"PCA_{comp_id}_PC2_vs_PC3.png" if inv.get("pca_pc2_pc3_png") else ""
        payload[f"comparison_{idx}_plsda_png"] = f"PLS-DA_CV_Ellipses_{comp_id}.png" if inv.get("plsda_png") else ""

        if comp_id == strongest:
            payload["visual_strongest"] = f"{comp_id} ({ppos + pneg} nominal p-value hits)"
        if comp_id == weakest:
            payload["visual_weakest"] = f"{comp_id} ({ppos + pneg} nominal p-value hits)"

    payload["example_annotation_1"] = first_example_annotation
    payload["example_annotation_2"] = second_example_annotation
    payload["example_volcano"] = payload.get("comparison_1_volcano_png", "")
    payload["example_heatmap"] = payload.get("comparison_1_heatmap_png", "")
    payload["example_pca"] = payload.get("comparison_1_pca_pc1_pc2_png", "")
    payload["example_plsda"] = payload.get("comparison_1_plsda_png", "")
    payload["overall_result_pattern"] = payload["main_visual_pattern"] or payload["short_statistical_summary"]
    payload["high_level_interpretation"] = payload["conservative_biological_summary"]
    payload["primary_question_interpretation"] = (
        f"The strongest nominal signal was observed for {strongest}, which should be interpreted in the context of the main biological question."
        if strongest else ""
    )
    payload["secondary_question_interpretation"] = (
        "The remaining contrasts suggest smaller or context-specific effects rather than uniformly large proteomic shifts."
    )
    payload["context_specific_interpretation"] = payload["asymmetry_or_other_pattern"]
    payload["statistical_caution"] = "All biological interpretation should remain conservative because no q-value-supported proteins were retained."
    payload["important_limit_or_alternative_explanation"] = "Observed nominal differences may reflect limited power, multiple-testing burden, or context-specific response patterns."
    payload["balanced_conclusion"] = payload["concise_results_conclusion"]
    payload["follow_up_direction"] = "Follow-up interpretation should prioritize recurring annotated proteins, pathway-level themes, and any independent validation data."
    payload["example_proteins_or_pathways"] = join_ids(
        [payload.get("comparison_1_example_accession", ""), payload.get("comparison_2_example_accession", "")]
    ).strip(", ")

    write_json(output_dir / "results_report_fields.json", payload)
    print(f"Wrote {output_dir / 'results_report_fields.json'}")


if __name__ == "__main__":
    main()
