#!/usr/bin/env python3
"""Extract a structured metadata summary for documentation autofill."""

from __future__ import annotations

import argparse
from pathlib import Path

from common import enabled_comparisons, group_factor_columns, included_rows, read_csv_rows, write_json


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--metadata-file", default="workflow/00_raw_data/config/sample_metadata.csv")
    parser.add_argument("--comparisons-file", default="workflow/00_raw_data/config/comparisons.csv")
    parser.add_argument("--output-dir", default="workflow/scripts/python/docs")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    metadata_file = Path(args.metadata_file).resolve()
    comparisons_file = Path(args.comparisons_file).resolve()
    output_dir = Path(args.output_dir).resolve()

    metadata_rows = read_csv_rows(metadata_file)
    included = included_rows(metadata_rows)
    factors = group_factor_columns(metadata_rows)

    groups = []
    seen_groups = sorted({row.get("group", "").strip() for row in included if row.get("group", "").strip()})
    for group_name in seen_groups:
        sample_ids = [row.get("sample_id", "").strip() for row in included if row.get("group", "").strip() == group_name]
        groups.append(
            {
                "group": group_name,
                "count": len(sample_ids),
                "sample_ids": sample_ids,
            }
        )

    factor_levels: dict[str, list[str]] = {}
    for factor in factors:
        factor_levels[factor] = sorted({row.get(factor, "").strip() for row in included if row.get(factor, "").strip()})

    comparison_rows = enabled_comparisons(read_csv_rows(comparisons_file))
    comparisons = []
    for row in comparison_rows:
        comparisons.append(
            {
                "comparison_id": row.get("comparison_id", "").strip(),
                "grouping_column": row.get("grouping_column", "").strip(),
                "group1": row.get("group1", "").strip(),
                "group2": row.get("group2", "").strip(),
                "label": f"{row.get('group1', '').strip()} vs. {row.get('group2', '').strip()}",
                "pvalue_cutoff": row.get("pvalue_cutoff", "").strip(),
                "qvalue_cutoff": row.get("qvalue_cutoff", "").strip(),
                "abs_log2fc_cutoff": row.get("abs_log2fc_cutoff", "").strip(),
            }
        )

    payload = {
        "sample_count": len(included),
        "sample_ids": [row.get("sample_id", "").strip() for row in included],
        "rows": [
            {
                "sample_id": row.get("sample_id", "").strip(),
                "group": row.get("group", "").strip(),
                **{factor: row.get(factor, "").strip() for factor in factors},
            }
            for row in included
        ],
        "factor_columns": factors,
        "factor_levels": factor_levels,
        "group_count": len(groups),
        "groups": groups,
        "enabled_comparison_count": len(comparisons),
        "comparisons": comparisons,
    }

    write_json(output_dir / "metadata_summary.json", payload)
    print(f"Wrote {output_dir / 'metadata_summary.json'}")


if __name__ == "__main__":
    main()
