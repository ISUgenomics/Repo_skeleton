#!/usr/bin/env python3
"""Extract a structured metadata summary for documentation autofill."""

from __future__ import annotations

import argparse
from pathlib import Path

from common import enabled_comparisons, group_factor_columns, included_rows, read_csv_rows, write_json


def build_sample_groups_table(groups: list[dict]) -> str:
    lines = [
        "| Group | Sample IDs | Count |",
        "|---|---|---|",
    ]
    for item in groups:
        sample_ids = ", ".join(item.get("sample_ids", []))
        lines.append(f"| `{item.get('group', '')}` | `{sample_ids}` | `{item.get('count', 0)}` |")
    return "\n".join(lines)


def interpretation_for(grouping_column: str, group1: str, group2: str) -> str:
    if grouping_column == "group":
        return "context-specific treatment effect within challenge"
    return f"main-effect contrast on {grouping_column}"


def count_for_value(rows: list[dict], column: str, value: str) -> int:
    return sum(1 for row in rows if row.get(column, "").strip() == value)


def build_requested_comparisons_table(comparisons: list[dict]) -> str:
    lines = [
        "| comparison_id | grouping_column | group1 | group2 |",
        "|---|---|---|---|",
    ]
    for row in comparisons:
        lines.append(
            f"| `{row.get('comparison_id', '')}` | `{row.get('grouping_column', '')}` | `{row.get('group1', '')}` | `{row.get('group2', '')}` |"
        )
    return "\n".join(lines)


def build_expected_comparisons_table(comparisons: list[dict], included_rows: list[dict]) -> str:
    lines = [
        "| Comparison | Interpretation | Group size |",
        "|---|---|---|",
    ]
    for row in comparisons:
        grouping_column = row.get("grouping_column", "")
        group1 = row.get("group1", "")
        group2 = row.get("group2", "")
        group1_count = count_for_value(included_rows, grouping_column, group1)
        group2_count = count_for_value(included_rows, grouping_column, group2)
        if group1_count and group1_count == group2_count:
            group_size = f"n={group1_count} per group"
        elif group1_count or group2_count:
            group_size = f"n={group1_count} vs n={group2_count}"
        else:
            group_size = ""
        lines.append(
            f"| `{row.get('comparison_id', '')}` | `{interpretation_for(grouping_column, group1, group2)}` | `{group_size}` |"
        )
    return "\n".join(lines)


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
        "sample_groups_table_md": build_sample_groups_table(groups),
        "enabled_comparison_count": len(comparisons),
        "comparisons": comparisons,
        "requested_comparisons_table_md": build_requested_comparisons_table(comparisons),
        "expected_comparisons_table_md": build_expected_comparisons_table(comparisons, included),
    }

    write_json(output_dir / "metadata_summary.json", payload)
    print(f"Wrote {output_dir / 'metadata_summary.json'}")


if __name__ == "__main__":
    main()
