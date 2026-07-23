#!/usr/bin/env python3
"""Extract a structured inventory of generated proteomics plot outputs."""

from __future__ import annotations

import argparse
from pathlib import Path

from common import enabled_comparisons, read_csv_rows, write_json


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--comparisons-file", default="workflow/00_raw_data/config/comparisons.csv")
    parser.add_argument("--output-root", default="workflow/03_visualization/output")
    parser.add_argument("--output-dir", default="workflow/scripts/python/docs")
    return parser.parse_args()


def present(path: Path) -> bool:
    return path.exists()


def comparison_inventory(output_root: Path, comparison_id: str) -> dict:
    html_dir = output_root / "HTML"
    png_dir = output_root / "PNG"
    svg_dir = output_root / "SVG"
    underscore_id = comparison_id
    hyphen_id = comparison_id.replace("_vs_", "-vs-")

    expected = {
        "volcano_p_png": png_dir / f"volcano_plot_{hyphen_id}_P.png",
        "volcano_q_png": png_dir / f"volcano_plot_{hyphen_id}_Q.png",
        "heatmap_p_png": png_dir / f"Heatmap_{underscore_id}_P.png",
        "pca_pc1_pc2_png": png_dir / f"PCA_{underscore_id}_PC1_vs_PC2.png",
        "pca_pc1_pc3_png": png_dir / f"PCA_{underscore_id}_PC1_vs_PC3.png",
        "pca_pc2_pc3_png": png_dir / f"PCA_{underscore_id}_PC2_vs_PC3.png",
        "plsda_png": png_dir / f"PLS-DA_CV_Ellipses_{underscore_id}.png",
        "volcano_p_html": html_dir / f"volcano_plot_{hyphen_id}_P.html",
        "volcano_q_html": html_dir / f"volcano_plot_{hyphen_id}_Q.html",
        "heatmap_p_html": html_dir / f"Heatmap_{underscore_id}_P.html",
        "pca_pc1_pc2_html": html_dir / f"PCA_{underscore_id}_PC1_vs_PC2.html",
        "pca_pc1_pc3_html": html_dir / f"PCA_{underscore_id}_PC1_vs_PC3.html",
        "pca_pc2_pc3_html": html_dir / f"PCA_{underscore_id}_PC2_vs_PC3.html",
        "pca_3d_html": html_dir / f"3D_PCA_{underscore_id}.html",
        "plsda_html": html_dir / f"PLS-DA_CV_Ellipses_{underscore_id}.html",
        "volcano_p_svg": svg_dir / f"volcano_plot_{hyphen_id}_P.svg",
        "volcano_q_svg": svg_dir / f"volcano_plot_{hyphen_id}_Q.svg",
        "heatmap_p_svg": svg_dir / f"Heatmap_{underscore_id}_P.svg",
        "pca_pc1_pc2_svg": svg_dir / f"PCA_{underscore_id}_PC1_vs_PC2.svg",
        "pca_pc1_pc3_svg": svg_dir / f"PCA_{underscore_id}_PC1_vs_PC3.svg",
        "pca_pc2_pc3_svg": svg_dir / f"PCA_{underscore_id}_PC2_vs_PC3.svg",
        "plsda_svg": svg_dir / f"PLS-DA_CV_Ellipses_{underscore_id}.svg",
    }

    files_present = {key: present(path) for key, path in expected.items()}
    html_count = sum(1 for key, is_present in files_present.items() if key.endswith("_html") and is_present)
    png_count = sum(1 for key, is_present in files_present.items() if key.endswith("_png") and is_present)
    svg_count = sum(1 for key, is_present in files_present.items() if key.endswith("_svg") and is_present)
    return {
        "comparison_id": comparison_id,
        "files_present": files_present,
        "counts": {
            "html": html_count,
            "png": png_count,
            "svg": svg_count,
        },
        "static_export_status": (
            "missing_all_exports" if html_count == 0 and png_count == 0 and svg_count == 0
            else "complete" if png_count > 0 and svg_count > 0
            else "missing_static_exports" if html_count > 0 and png_count == 0 and svg_count == 0
            else "partial"
        ),
    }


def main() -> None:
    args = parse_args()
    comparisons_file = Path(args.comparisons_file).resolve()
    output_root = Path(args.output_root).resolve()
    output_dir = Path(args.output_dir).resolve()

    comparison_rows = enabled_comparisons(read_csv_rows(comparisons_file))
    comparison_ids = [row.get("comparison_id", "").strip() for row in comparison_rows if row.get("comparison_id", "").strip()]

    comparisons = {comparison_id: comparison_inventory(output_root, comparison_id) for comparison_id in comparison_ids}

    payload = {
        "comparison_count": len(comparisons),
        "comparisons": comparisons,
        "aggregate": {
            "volcano_plots_generated": sum(1 for item in comparisons.values() if item["files_present"].get("volcano_p_png")),
            "heatmaps_generated": sum(1 for item in comparisons.values() if item["files_present"].get("heatmap_p_png")),
            "pca_plots_generated": sum(1 for item in comparisons.values() if item["files_present"].get("pca_pc1_pc2_png")),
            "pca_3d_plots_generated": sum(1 for item in comparisons.values() if item["files_present"].get("pca_3d_html")),
            "plsda_plots_generated": sum(1 for item in comparisons.values() if item["files_present"].get("plsda_png")),
            "html_exports_present": sum(item["counts"]["html"] for item in comparisons.values()),
            "png_exports_present": sum(item["counts"]["png"] for item in comparisons.values()),
            "svg_exports_present": sum(item["counts"]["svg"] for item in comparisons.values()),
            "static_export_issue_count": sum(1 for item in comparisons.values() if item.get("static_export_status") != "complete"),
        },
    }

    write_json(output_dir / "visualization_inventory.json", payload)
    print(f"Wrote {output_dir / 'visualization_inventory.json'}")


if __name__ == "__main__":
    main()
