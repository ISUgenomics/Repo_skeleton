#!/usr/bin/env python3
"""Extract a structured statistics summary from proteomics comparison outputs."""

from __future__ import annotations

import argparse
from pathlib import Path

from common import read_csv_rows, safe_float, write_json


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--stats-dir", default="workflow/02_statistics/CSV")
    parser.add_argument("--counts-file", default="workflow/02_statistics/significant_protein_counts.csv")
    parser.add_argument("--output-dir", default="workflow/scripts/python/docs")
    parser.add_argument("--p-cutoff", type=float, default=0.05)
    parser.add_argument("--q-cutoff", type=float, default=0.05)
    parser.add_argument("--abs-log2fc-cutoff", type=float, default=1.0)
    return parser.parse_args()


def normalize_comparison_id(text: str) -> str:
    return text.strip().replace(" vs. ", "_vs_").replace(" vs ", "_vs_")


def summarize_comparison(csv_path: Path, p_cutoff: float, q_cutoff: float, abs_log2fc_cutoff: float) -> dict:
    rows = read_csv_rows(csv_path)
    p_pos = p_neg = q_pos = q_neg = 0
    example_hits = []

    for row in rows:
        log2fc = safe_float(row.get("log2FoldChange"))
        p_value = safe_float(row.get("p-value_StudentTtest"))
        q_value = safe_float(row.get("q-value_StudentTtest"))
        if log2fc is None or p_value is None or q_value is None:
            continue
        if abs(log2fc) <= abs_log2fc_cutoff:
            continue
        accession = row.get("") or row.get("Accession") or row.get("Feature") or ""
        description = row.get("Description", "")
        if p_value < p_cutoff:
            if log2fc > 0:
                p_pos += 1
            elif log2fc < 0:
                p_neg += 1
            if len(example_hits) < 5:
                example_hits.append(
                    {
                        "accession": accession,
                        "description": description,
                        "fold_change": "positive" if log2fc > 0 else "negative",
                        "p_value": p_value,
                        "q_value": q_value,
                    }
                )
        if q_value < q_cutoff:
            if log2fc > 0:
                q_pos += 1
            elif log2fc < 0:
                q_neg += 1

    return {
        "comparison_csv": csv_path.name,
        "p_positive_hits": p_pos,
        "p_negative_hits": p_neg,
        "q_positive_hits": q_pos,
        "q_negative_hits": q_neg,
        "example_hits": example_hits,
    }


def main() -> None:
    args = parse_args()
    stats_dir = Path(args.stats_dir).resolve()
    counts_file = Path(args.counts_file).resolve()
    output_dir = Path(args.output_dir).resolve()

    counts_rows = read_csv_rows(counts_file)
    counts_by_comparison = {}
    for row in counts_rows:
        raw_name = row.get("Comparison", "").strip()
        if not raw_name:
            continue
        counts_by_comparison[normalize_comparison_id(raw_name)] = {
            "significant_p_hits": int(float(row.get("Proteins with significant pvalue", "0") or 0)),
            "significant_q_hits": int(float(row.get("Proteins with significant qvalue", "0") or 0)),
        }

    comparisons: dict[str, dict] = {}
    for csv_path in sorted(stats_dir.glob("*_comparison.csv")):
        comparison_id = csv_path.name.removesuffix("_comparison.csv")
        summary = summarize_comparison(csv_path, args.p_cutoff, args.q_cutoff, args.abs_log2fc_cutoff)
        summary.update(counts_by_comparison.get(comparison_id, {}))
        if "significant_p_hits" not in summary:
            summary["significant_p_hits"] = summary["p_positive_hits"] + summary["p_negative_hits"]
        if "significant_q_hits" not in summary:
            summary["significant_q_hits"] = summary["q_positive_hits"] + summary["q_negative_hits"]
        comparisons[comparison_id] = summary

    strongest = None
    weakest = None
    for comparison_id, summary in comparisons.items():
        p_hits = int(summary.get("significant_p_hits", 0))
        if strongest is None or p_hits > strongest[1]:
            strongest = (comparison_id, p_hits)
        if weakest is None or p_hits < weakest[1]:
            weakest = (comparison_id, p_hits)

    payload = {
        "comparison_count": len(comparisons),
        "strongest_nominal_comparison": strongest[0] if strongest else "",
        "strongest_nominal_hits": strongest[1] if strongest else 0,
        "weakest_nominal_comparison": weakest[0] if weakest else "",
        "weakest_nominal_hits": weakest[1] if weakest else 0,
        "comparisons": comparisons,
    }

    write_json(output_dir / "statistics_summary.json", payload)
    print(f"Wrote {output_dir / 'statistics_summary.json'}")


if __name__ == "__main__":
    main()
