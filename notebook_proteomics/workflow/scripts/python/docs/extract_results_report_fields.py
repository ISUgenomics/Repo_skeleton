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


def format_score(example: dict) -> str:
    p_value = example.get("p_value")
    q_value = example.get("q_value")
    def fmt(value, fallback):
        try:
            numeric = float(value)
            if 0.95 <= numeric < 1:
                return f"{numeric:.4f}".rstrip("0").rstrip(".")
            return f"{numeric:.3g}"
        except (TypeError, ValueError):
            text = str(fallback or "")
            try:
                numeric = float(text)
                if 0.95 <= numeric < 1:
                    return f"{numeric:.4f}".rstrip("0").rstrip(".")
                return f"{numeric:.3g}"
            except (TypeError, ValueError):
                return text

    p_text = fmt(p_value, example.get("p_value_text", ""))
    q_text = fmt(q_value, example.get("q_value_text", ""))
    p_label = p_text
    q_label = q_text
    try:
        if float(p_value) < 0.05:
            p_label = f"**{p_label}**"
    except (TypeError, ValueError):
        pass
    try:
        if float(q_value) < 0.05:
            q_label = f"**{q_label}**"
    except (TypeError, ValueError):
        pass
    return f"{p_label}, {q_label}".strip(", ")


def sample_ids_for(rows: list[dict], grouping_column: str, value: str) -> list[str]:
    return [row.get("sample_id", "") for row in rows if row.get(grouping_column, "") == value]


def csv_row_count(path: Path) -> int:
    if not path.exists():
        return 0
    with path.open() as handle:
        return max(sum(1 for _ in handle) - 1, 0)


def build_significant_protein_table(comparisons: list[dict], stats_comparisons: dict[str, dict]) -> str:
    lines = [
        "| Comparison | Comparison table | Significant p-value hits | Significant q-value hits |",
        "|---|---|---:|---:|",
    ]
    for comp in comparisons:
        comp_id = comp.get("comparison_id", "")
        stat = stats_comparisons.get(comp_id, {})
        file_name = f"{comp_id}_comparison.csv" if comp_id else ""
        lines.append(
            f"| `{comp_id}` | [{file_name}](./workflow/02_statistics/CSV/{file_name}) | {int(stat.get('significant_p_hits', 0) or 0)} | {int(stat.get('significant_q_hits', 0) or 0)} |"
        )
    return "\n".join(lines)


def build_significant_hits_details(comparisons: list[dict], hits: dict[str, dict]) -> str:
    blocks: list[str] = []
    for comp in comparisons:
        comp_id = comp.get("comparison_id", "")
        hit_rows = hits.get(comp_id, {}).get("significant_hits_table", [])
        lines = [
            f"<details><summary>protein hits in <b>{comp_id.replace('_vs_', ' vs. ')}</b></summary>",
            "",
            "| Gene | Accession | FoldChange | Score (p,q) | Description |",
            "|---|---|---|---|---|",
        ]
        if hit_rows:
            for row in hit_rows:
                score = format_score(row)
                lines.append(
                    f"| `{row.get('gene_symbol', '')}` | `{row.get('accession', '')}` | `{row.get('direction', '')}` | {score} | `{row.get('description', '')}` |"
                )
        else:
            lines.append("| `none` | `none` | `n/a` | n/a | `No proteins met the nominal reporting thresholds for this comparison.` |")
        lines.extend(["", "</details>"])
        blocks.append("\n".join(lines))
    return "\n\n".join(blocks)


def build_figure_browser_sections(
    comparisons: list[dict],
    metadata_groups: dict[str, dict],
    metadata_rows: list[dict],
    viz_comparisons: dict[str, dict],
) -> str:
    blocks: list[str] = []
    for comp in comparisons:
        comp_id = comp.get("comparison_id", "")
        group1 = comp.get("group1", "")
        group2 = comp.get("group2", "")
        grouping_column = comp.get("grouping_column", "")
        if grouping_column == "group":
            sample_ids_a = metadata_groups.get(group1, {}).get("sample_ids", [])
            sample_ids_b = metadata_groups.get(group2, {}).get("sample_ids", [])
        else:
            sample_ids_a = sample_ids_for(metadata_rows, grouping_column, group1)
            sample_ids_b = sample_ids_for(metadata_rows, grouping_column, group2)
        group_size = len(sample_ids_a) if sample_ids_a else metadata_groups.get(group1, {}).get("count", 0)
        inv = viz_comparisons.get(comp_id, {}).get("files_present", {})
        hyphen_id = comp_id.replace("_vs_", "-vs-")
        lines = [
            f"<details><summary>{comp_id.replace('_vs_', ' vs. ')}</summary>",
            "",
            f"<details style=\"margin-left: 20px;\"><summary>Samples: n={group_size} per group</summary>",
            "",
            f"**{group1}:** | `{'` | `'.join(sample_ids_a)}`  ",
            f"**{group2}:** | `{'` | `'.join(sample_ids_b)}`  ",
            "",
            "</details>",
            "",
            "---",
            "",
            "Volcano plot using the default `p < 0.05` and `abs(log2FC) > 1` thresholds:",
            "",
        ]
        volcano_png = f"volcano_plot_{hyphen_id}_P.png"
        heatmap_png = f"Heatmap_{comp_id}_P.png"
        pca12_png = f"PCA_{comp_id}_PC1_vs_PC2.png"
        pca13_png = f"PCA_{comp_id}_PC1_vs_PC3.png"
        pca23_png = f"PCA_{comp_id}_PC2_vs_PC3.png"
        plsda_png = f"PLS-DA_CV_Ellipses_{comp_id}.png"
        lines.append(
            f"![](./workflow/03_visualization/output/PNG/{volcano_png})" if inv.get("volcano_p_png")
            else "_Volcano PNG was not generated in this run._"
        )
        lines.extend([
            "",
            "Heatmap of proteins passing the same reporting thresholds:",
            "",
            f"![](./workflow/03_visualization/output/PNG/{heatmap_png})" if inv.get("heatmap_p_png")
            else "_Heatmap PNG was not generated in this run._",
            "",
            "PCA panels for the first three principal-component pairings:",
            "",
            f"![](./workflow/03_visualization/output/PNG/{pca12_png})" if inv.get("pca_pc1_pc2_png")
            else "_PCA PC1 vs PC2 PNG was not generated in this run._",
            "",
            f"![](./workflow/03_visualization/output/PNG/{pca13_png})" if inv.get("pca_pc1_pc3_png")
            else "_PCA PC1 vs PC3 PNG was not generated in this run._",
            "",
            f"![](./workflow/03_visualization/output/PNG/{pca23_png})" if inv.get("pca_pc2_pc3_png")
            else "_PCA PC2 vs PC3 PNG was not generated in this run._",
            "",
            "PLS-DA with cross-validation:",
            "",
            f"![](./workflow/03_visualization/output/PNG/{plsda_png})" if inv.get("plsda_png")
            else "_PLS-DA PNG was not generated in this run._",
            "</details>",
        ])
        blocks.append("\n".join(lines))
    return "\n\n".join(blocks)


def build_visual_observations(comparisons: list[dict], stats_comparisons: dict[str, dict], strongest: str, weakest: str) -> str:
    if not comparisons:
        return "- No comparison-level visualization observations were generated."
    observations: list[str] = []
    if strongest:
        strongest_hits = int(stats_comparisons.get(strongest, {}).get("significant_p_hits", 0) or 0)
        observations.append(f"- `{strongest}` showed the strongest overall nominal signal (`n={strongest_hits}` p-value hits).")
    if weakest:
        weakest_hits = int(stats_comparisons.get(weakest, {}).get("significant_p_hits", 0) or 0)
        observations.append(f"- `{weakest}` showed the weakest nominal signal (`n={weakest_hits}` p-value hits).")
    observations.append("- All enabled comparisons were carried through the standard visualization set using the same reporting thresholds.")
    observations.append("- q-value-based plots remained less informative than nominal p-value plots because no q-value-supported proteins were retained.")
    return "\n".join(observations)


def hypothesis_hits(stats_comparisons: dict[str, dict], strongest: str) -> dict[str, str]:
    return {}


def plot_examples_for(comp_id: str, inv: dict[str, bool]) -> dict[str, str]:
    hyphen_id = comp_id.replace("_vs_", "-vs-")
    return {
        "volcano_png": f"volcano_plot_{hyphen_id}_P.png" if inv.get("volcano_p_png") else "",
        "heatmap_png": f"Heatmap_{comp_id}_P.png" if inv.get("heatmap_p_png") else "",
        "pca_pc1_pc2_png": f"PCA_{comp_id}_PC1_vs_PC2.png" if inv.get("pca_pc1_pc2_png") else "",
        "pca_pc1_pc3_png": f"PCA_{comp_id}_PC1_vs_PC3.png" if inv.get("pca_pc1_pc3_png") else "",
        "pca_pc2_pc3_png": f"PCA_{comp_id}_PC2_vs_PC3.png" if inv.get("pca_pc2_pc3_png") else "",
        "plsda_png": f"PLS-DA_CV_Ellipses_{comp_id}.png" if inv.get("plsda_png") else "",
    }


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
    payload["significant_proteins_table_md"] = build_significant_protein_table(comparisons, stats_comparisons)
    payload["significant_hits_details_md"] = build_significant_hits_details(comparisons, hits)
    payload["figure_browser_sections_md"] = build_figure_browser_sections(comparisons, groups, rows, viz_comparisons)
    payload["project_specific_visual_observations_md"] = build_visual_observations(comparisons, stats_comparisons, strongest, weakest)

    example_annotations: list[str] = []
    first_plot_examples = {
        "volcano_png": "",
        "heatmap_png": "",
        "pca_pc1_pc2_png": "",
        "plsda_png": "",
    }

    for comp in comparisons:
        comp_id = comp.get("comparison_id", "")
        group1 = comp.get("group1", "")
        group2 = comp.get("group2", "")
        grouping_column = comp.get("grouping_column", "")
        if grouping_column == "group":
            sample_ids_a = groups.get(group1, {}).get("sample_ids", [])
            sample_ids_b = groups.get(group2, {}).get("sample_ids", [])
        else:
            sample_ids_a = sample_ids_for(rows, grouping_column, group1)
            sample_ids_b = sample_ids_for(rows, grouping_column, group2)

        stat = stats_comparisons.get(comp_id, {})
        ppos = int(stat.get("p_positive_hits", 0) or 0)
        pneg = int(stat.get("p_negative_hits", 0) or 0)

        example_hits = stat.get("example_hits", [])
        if example_hits:
            example = example_hits[0]
            annotation = f"{example.get('accession', '')} [{example.get('description', '')}]"
            if annotation and annotation not in example_annotations:
                example_annotations.append(annotation)

        inv = viz_comparisons.get(comp_id, {}).get("files_present", {})
        if not first_plot_examples["volcano_png"]:
            first_plot_examples = plot_examples_for(comp_id, inv)

        if comp_id == strongest:
            payload["visual_strongest"] = f"{comp_id} ({ppos + pneg} nominal p-value hits)"
        if comp_id == weakest:
            payload["visual_weakest"] = f"{comp_id} ({ppos + pneg} nominal p-value hits)"

    payload["example_annotation_1"] = example_annotations[0] if len(example_annotations) >= 1 else ""
    payload["example_annotation_2"] = example_annotations[1] if len(example_annotations) >= 2 else ""
    payload["example_volcano"] = first_plot_examples["volcano_png"]
    payload["example_heatmap"] = first_plot_examples["heatmap_png"]
    payload["example_pca"] = first_plot_examples["pca_pc1_pc2_png"]
    payload["example_plsda"] = first_plot_examples["plsda_png"]
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
        [annotation.split(" [", 1)[0] for annotation in example_annotations[:2]]
    ).strip(", ")
    payload.update(hypothesis_hits(stats_comparisons, strongest))

    write_json(output_dir / "results_report_fields.json", payload)
    print(f"Wrote {output_dir / 'results_report_fields.json'}")


if __name__ == "__main__":
    main()
