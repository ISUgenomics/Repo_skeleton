#!/usr/bin/env python3
"""Extract a compact run summary from manifest, metadata, stats, and plot summaries."""

from __future__ import annotations

import argparse
from pathlib import Path

from common import parse_manifest_yaml, read_json, write_json


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--manifest-file", default="workflow/00_raw_data/config/project_manifest.yaml")
    parser.add_argument("--metadata-summary", default="workflow/scripts/python/docs/metadata_summary.json")
    parser.add_argument("--statistics-summary", default="workflow/scripts/python/docs/statistics_summary.json")
    parser.add_argument("--visualization-summary", default="workflow/scripts/python/docs/visualization_inventory.json")
    parser.add_argument("--software-versions", default="workflow/01_qc_normalization/software_versions.txt")
    parser.add_argument("--output-dir", default="workflow/scripts/python/docs")
    return parser.parse_args()


def parse_versions(path: Path) -> dict[str, str]:
    if not path.exists():
        return {}
    result: dict[str, str] = {}
    for line in path.read_text().splitlines():
        if "\t" in line:
            key, value = line.split("\t", 1)
        elif ":" in line:
            key, value = line.split(":", 1)
        else:
            continue
        result[key.strip()] = value.strip()
    return result


def main() -> None:
    args = parse_args()
    manifest = parse_manifest_yaml(Path(args.manifest_file).resolve())
    metadata_summary = read_json(Path(args.metadata_summary).resolve()) or {}
    statistics_summary = read_json(Path(args.statistics_summary).resolve()) or {}
    visualization_summary = read_json(Path(args.visualization_summary).resolve()) or {}
    software_versions = parse_versions(Path(args.software_versions).resolve())
    output_dir = Path(args.output_dir).resolve()
    viz_aggregate = visualization_summary.get("aggregate", {})
    html_exports = int(viz_aggregate.get("html_exports_present", 0) or 0)
    png_exports = int(viz_aggregate.get("png_exports_present", 0) or 0)
    svg_exports = int(viz_aggregate.get("svg_exports_present", 0) or 0)
    comparison_count = int(visualization_summary.get("comparison_count", 0) or 0)
    plot_outputs_missing = comparison_count > 0 and html_exports == 0 and png_exports == 0 and svg_exports == 0
    static_missing = html_exports > 0 and png_exports == 0 and svg_exports == 0

    payload = {
        "project": manifest.get("project", {}),
        "inputs": manifest.get("inputs", {}),
        "analysis": manifest.get("analysis", {}),
        "metadata_summary": metadata_summary,
        "statistics_summary": statistics_summary,
        "visualization_summary": visualization_summary,
        "software_versions": software_versions,
        "final_run_status": (
            "failed" if plot_outputs_missing else
            "complete_with_warnings" if static_missing else
            "complete"
        ) if metadata_summary and statistics_summary and visualization_summary else "partial",
    }

    write_json(output_dir / "run_summary.json", payload)
    print(f"Wrote {output_dir / 'run_summary.json'}")


if __name__ == "__main__":
    main()
