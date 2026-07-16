#!/usr/bin/env python3
"""Extract significant-hit summaries from proteomics comparison CSV files.

This helper is intended for documentation/report autofill workflows.
It reads comparison CSV files, applies the standard p-value / q-value /
absolute log2 fold-change thresholds, and writes a compact JSON summary
that can be reused in project *.md reports.
"""

from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--input-dir",
        default="workflow/02_statistics/CSV",
        help="Directory containing *_comparison.csv files.",
    )
    parser.add_argument(
        "--output-dir",
        default="workflow/scripts/python/docs",
        help="Directory where summary files should be written.",
    )
    parser.add_argument("--p-cutoff", type=float, default=0.05)
    parser.add_argument("--q-cutoff", type=float, default=0.05)
    parser.add_argument("--abs-log2fc-cutoff", type=float, default=1.0)
    return parser.parse_args()


def read_hits(csv_path: Path, p_cutoff: float, q_cutoff: float, abs_log2fc_cutoff: float) -> dict:
    p_hits = []
    q_hits = []
    merged_hits = {}
    with csv_path.open(newline="") as handle:
        reader = csv.DictReader(handle)
        for row in reader:
            accession = row.get("") or row.get("Accession") or row.get("Feature") or ""
            gene_symbol = row.get("Gene Symbol") or row.get("GeneSymbol") or row.get("Feature") or accession
            description = row.get("Description", "")
            try:
                p_value = float(row["p-value_StudentTtest"])
                q_value = float(row["q-value_StudentTtest"])
                abs_log2fc = abs(float(row["log2FoldChange"]))
            except (KeyError, TypeError, ValueError):
                continue

            hit = {
                "accession": accession,
                "gene_symbol": gene_symbol,
                "description": description,
                "p_value": p_value,
                "q_value": q_value,
                "direction": "positive" if float(row["log2FoldChange"]) > 0 else "negative",
                "abs_log2fc": abs_log2fc,
            }
            if p_value < p_cutoff and abs_log2fc > abs_log2fc_cutoff:
                p_hits.append(hit)
                merged = merged_hits.setdefault(
                    accession,
                    {
                        "accession": accession,
                        "gene_symbol": gene_symbol,
                        "description": description,
                        "direction": hit["direction"],
                        "evidence": [],
                        "p_value": p_value,
                        "q_value": q_value,
                    },
                )
                merged["evidence"].append("p-value")
            if q_value < q_cutoff and abs_log2fc > abs_log2fc_cutoff:
                q_hits.append(hit)
                merged = merged_hits.setdefault(
                    accession,
                    {
                        "accession": accession,
                        "gene_symbol": gene_symbol,
                        "description": description,
                        "direction": hit["direction"],
                        "evidence": [],
                        "p_value": p_value,
                        "q_value": q_value,
                    },
                )
                merged["evidence"].append("q-value")

    merged_hits_list = []
    for hit in merged_hits.values():
        hit["evidence"] = "|".join(hit["evidence"])
        merged_hits_list.append(hit)
    merged_hits_list.sort(key=lambda item: (item["q_value"], item["p_value"], item["accession"]))

    return {
        "comparison_csv": csv_path.name,
        "significant_p_hits": p_hits,
        "significant_q_hits": q_hits,
        "significant_hits_table": merged_hits_list,
    }


def main() -> None:
    args = parse_args()
    input_dir = Path(args.input_dir).resolve()
    output_dir = Path(args.output_dir).resolve()
    output_dir.mkdir(parents=True, exist_ok=True)

    summary = {}
    for csv_path in sorted(input_dir.glob("*_comparison.csv")):
        comparison_id = csv_path.name.removesuffix("_comparison.csv")
        summary[comparison_id] = read_hits(
            csv_path=csv_path,
            p_cutoff=args.p_cutoff,
            q_cutoff=args.q_cutoff,
            abs_log2fc_cutoff=args.abs_log2fc_cutoff,
        )

    json_path = output_dir / "significant_hits_summary.json"
    json_path.write_text(json.dumps(summary, indent=2) + "\n")

    print(f"Wrote {json_path}")


if __name__ == "__main__":
    main()
