#!/usr/bin/env python3
"""Shared helpers for proteomics documentation extractors."""

from __future__ import annotations

import csv
import json
from pathlib import Path
from typing import Any


def read_csv_rows(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open(newline="") as handle:
        return list(csv.DictReader(handle))


def write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2) + "\n")


def read_json(path: Path) -> Any | None:
    if not path.exists():
        return None
    return json.loads(path.read_text())


def parse_manifest_yaml(path: Path) -> dict[str, Any]:
    root: dict[str, Any] = {}
    current_section: str | None = None
    for raw in path.read_text().splitlines():
        if not raw.strip() or raw.lstrip().startswith("#"):
            continue
        if not raw.startswith(" "):
            if raw.rstrip().endswith(":"):
                current_section = raw.rstrip()[:-1]
                root[current_section] = {}
            continue
        if current_section and raw.startswith("  ") and ":" in raw:
            key, value = raw.strip().split(":", 1)
            value = value.split("#", 1)[0].strip().strip('"').strip("'")
            root[current_section][key] = value
    return root


def included_rows(rows: list[dict[str, str]]) -> list[dict[str, str]]:
    return [row for row in rows if str(row.get("include", "")).strip().upper() == "TRUE"]


def enabled_comparisons(rows: list[dict[str, str]]) -> list[dict[str, str]]:
    return [row for row in rows if str(row.get("enabled", "")).strip().upper() == "TRUE"]


def group_factor_columns(rows: list[dict[str, str]]) -> list[str]:
    if not rows:
        return []
    excluded = {"sample_id", "source_column", "group", "replicate", "batch_or_run", "include", "notes", "column_name"}
    return [col for col in rows[0].keys() if col not in excluded]


def safe_float(value: str | None) -> float | None:
    try:
        return float(value) if value not in (None, "") else None
    except (TypeError, ValueError):
        return None
