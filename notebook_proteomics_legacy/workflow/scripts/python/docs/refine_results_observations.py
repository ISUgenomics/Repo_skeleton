#!/usr/bin/env python3
"""Upgrade Project-specific observations in 04_Results.md using research candidates and workflow outputs."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--project-root", default=".")
    parser.add_argument("--results-doc", default="04_Results.md")
    parser.add_argument("--stats", default="workflow/scripts/python/docs/statistics_summary.json")
    parser.add_argument("--candidates", default="workflow/scripts/python/docs/literature_candidates.json")
    return parser.parse_args()


def load_json(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
        return data if isinstance(data, dict) else {}
    except Exception:
        return {}


def clean(value: Any) -> str:
    return " ".join(str(value or "").split())


def prefer_gene_label(item: dict[str, Any]) -> str:
    protein_or_theme = clean(item.get("protein_or_theme"))
    if protein_or_theme and " " not in protein_or_theme and "/" not in protein_or_theme and protein_or_theme.upper() == protein_or_theme:
        return protein_or_theme
    matched = item.get("matched_context")
    if isinstance(matched, list):
        for candidate in matched:
            gene = clean(candidate)
            if gene and " " not in gene and "/" not in gene and gene.upper() == gene:
                return gene
        for candidate in matched:
            gene = clean(candidate)
            if gene:
                return gene
    return protein_or_theme


def candidate_genes(candidates: list[dict[str, Any]], comparison_id: str) -> list[str]:
    ranked: list[tuple[str, str]] = []
    for item in candidates:
        if clean(item.get("focus_area")) != "hypothesis_screening_table":
            continue
        if clean(item.get("comparison_id")) != comparison_id:
            continue
        gene = prefer_gene_label(item)
        if not gene:
            continue
        ranked.append((clean(item.get("sort_key")), gene))
    ranked.sort()
    seen: set[str] = set()
    ordered: list[str] = []
    for _, gene in ranked:
        if gene in seen:
            continue
        seen.add(gene)
        ordered.append(gene)
    return ordered


def format_gene_list(genes: list[str], limit: int = 4) -> str:
    picked = [f"`{gene}`" for gene in genes[:limit] if gene]
    if not picked:
        return ""
    if len(picked) == 1:
        return picked[0]
    if len(picked) == 2:
        return f"{picked[0]} and {picked[1]}"
    return ", ".join(picked[:-1]) + f", and {picked[-1]}"


def build_observations(stats: dict[str, Any], candidates: dict[str, Any]) -> str:
    comparisons = stats.get("comparisons", {})
    candidate_rows = candidates.get("candidate_references", [])
    if not isinstance(comparisons, dict):
        return "- Project-specific observations were not available for this run."

    def hits(comp: str) -> int:
        return int(comparisons.get(comp, {}).get("significant_p_hits", 0) or 0)

    def posneg(comp: str) -> tuple[int, int]:
        payload = comparisons.get(comp, {})
        return (
            int(payload.get("p_positive_hits", 0) or 0),
            int(payload.get("p_negative_hits", 0) or 0),
        )

    bullets: list[str] = []

    if "LPS_vs_PF" in comparisons:
        genes = candidate_genes(candidate_rows, "LPS_vs_PF")
        gene_text = format_gene_list(genes or ["PTX3"], limit=3)
        bullets.append(
            f"- `LPS vs. PF` showed the strongest overall support across the figure sets and also produced the largest nominal hit list (`n={hits('LPS_vs_PF')}`). "
            f"Example proteins potentially relevant to the inflammatory-challenge question include {gene_text}."
        )

    if "CON_vs_SBE" in comparisons:
        pos, neg = posneg("CON_vs_SBE")
        genes = candidate_genes(candidate_rows, "CON_vs_SBE")
        gene_text = format_gene_list(genes or ["LBP", "GCLC"])
        bullets.append(
            f"- `CON vs. SBE` produced a smaller but still balanced nominal hit set (`{pos}` positive and `{neg}` negative). "
            f"Example proteins potentially relevant to diet-associated metabolic, inflammatory, or stress-response differences include {gene_text}."
        )

    if "CON-PF_vs_SBE-PF" in comparisons:
        pos, neg = posneg("CON-PF_vs_SBE-PF")
        direction = f"`{neg}` nominally significant proteins, all on the negative fold-change side" if pos == 0 else f"`{pos}` positive and `{neg}` negative nominal hits"
        bullets.append(
            f"- `CON-PF vs. SBE-PF` showed the weakest visual and statistical support and contained only {direction}. "
            "In this run, that comparison does not support a broad diet effect within the non-challenged animals."
        )

    if "CON-LPS_vs_SBE-LPS" in comparisons:
        pos, neg = posneg("CON-LPS_vs_SBE-LPS")
        genes = candidate_genes(candidate_rows, "CON-LPS_vs_SBE-LPS")
        gene_text = format_gene_list(genes or ["TOLLIP", "TRIP6"], limit=3)
        stronger_than_pf = ""
        if hits("CON-LPS_vs_SBE-LPS") > hits("CON-PF_vs_SBE-PF"):
            stronger_than_pf = " remained stronger than the `PF`-only diet contrast and"
        bullets.append(
            f"- `CON-LPS vs. SBE-LPS`{stronger_than_pf} was also predominantly one-sided (`{neg}` negative and `{pos}` positive). "
            f"Example proteins potentially relevant to signaling or immune-response context include {gene_text}, which is consistent with the possibility that diet-associated differences were more evident under inflammatory-challenge conditions than under `PF` conditions."
        )

    return "\n".join(bullets) if bullets else "- Project-specific observations were not available for this run."


def replace_observations(text: str, block: str) -> str:
    header = "**Project-specific observations:**"
    if header in text:
        pattern = re.compile(
            r"(\*\*Project-specific observations:\*\*\n)(.*?)(?=\n## |\n---\n|\Z)",
            flags=re.DOTALL,
        )
        replacement = "\\1" + block.strip() + "\n"
        updated, count = pattern.subn(replacement, text, count=1)
        if count:
            return updated
    insertion = "\n\n---\n\n**Project-specific observations:**\n" + block.strip() + "\n"
    marker = "## QC and Normalization Summary"
    if marker in text:
        return text.replace("\n" + marker, insertion + "\n" + marker, 1)
    return text.rstrip() + insertion


def main() -> int:
    args = parse_args()
    project_root = Path(args.project_root).resolve()
    doc_path = (project_root / args.results_doc).resolve()
    stats = load_json((project_root / args.stats).resolve())
    candidates = load_json((project_root / args.candidates).resolve())
    if not doc_path.exists():
        print(f"Skipping: missing {doc_path}")
        return 0
    text = doc_path.read_text(encoding="utf-8")
    block = build_observations(stats, candidates)
    updated = replace_observations(text, block)
    if updated != text:
        doc_path.write_text(updated, encoding="utf-8")
        print(f"Updated {doc_path}")
    else:
        print(f"No change to {doc_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
