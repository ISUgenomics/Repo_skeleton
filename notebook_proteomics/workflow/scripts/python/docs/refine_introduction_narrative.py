#!/usr/bin/env python3
"""Lightly refine the generated Introduction summary using resolved project context.

This script rewrites only the ``## Manuscript-Style Summary`` section of
``05_Introduction.md``. It is intended for research mode so deterministic docs
remain intact while the generated narrative becomes cleaner and more readable.
"""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--project-root", default=".")
    parser.add_argument("--values", default="template/variables.values.json")
    parser.add_argument("--project-context", default="workflow/scripts/python/docs/project_context.json")
    parser.add_argument("--input-doc", default="05_Introduction.md")
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
    return " ".join(str(value or "").replace("_vs_", " vs. ").split())


def infer_semantic_labels(values: dict[str, Any]) -> dict[str, str]:
    context = clean(values.get("key_correspondence_excerpt")) or clean(values.get("text_context_context"))
    organism = clean(values.get("organism_or_system"))
    if organism.lower() == "bos taurus" and "holstein cows" in context.lower():
        organism = "mature lactating Holstein cows"

    primary_factor = clean(values.get("primary_factor_name"))
    if primary_factor.lower() == "treatment" and "two levels of diet" in context.lower():
        primary_factor = "diet"

    secondary_factor = clean(values.get("secondary_factor_name"))
    if not secondary_factor:
        secondary_factor = "challenge"

    primary_detail = ""
    if "con=dietary control" in context.lower():
        primary_detail = "cows were assigned to either a control diet (`CON`) or a polyphenol-supplemented diet (`SBE`)"

    secondary_detail = ""
    if "challenged with lps" in context.lower() and "pair-fed (pf)" in context.lower():
        secondary_detail = "cows challenged with `LPS` and non-challenged intake-matched controls (`PF`)"

    return {
        "organism": organism,
        "primary_factor": primary_factor,
        "secondary_factor": secondary_factor,
        "primary_detail": primary_detail,
        "secondary_detail": secondary_detail,
        "context": context,
    }


def section_bounds(text: str, heading: str) -> tuple[int, int] | None:
    match = re.search(rf"^##\s+{re.escape(heading)}\s*$", text, flags=re.MULTILINE)
    if not match:
        return None
    start = match.end()
    next_heading = re.search(r"^##\s+", text[start:], flags=re.MULTILINE)
    end = len(text) if not next_heading else start + next_heading.start()
    return start, end


def ensure_section(text: str, heading: str) -> tuple[str, tuple[int, int]]:
    bounds = section_bounds(text, heading)
    if bounds is not None:
        return text, bounds
    if text and not text.endswith("\n"):
        text += "\n"
    if text and not text.endswith("\n\n"):
        text += "\n"
    text += f"## {heading}\n\n"
    bounds = section_bounds(text, heading)
    assert bounds is not None
    return text, bounds


def oxford_join(values: list[str]) -> str:
    values = [clean(v) for v in values if clean(v)]
    if not values:
        return ""
    if len(values) == 1:
        return values[0]
    if len(values) == 2:
        return f"{values[0]} and {values[1]}"
    return f"{', '.join(values[:-1])}, and {values[-1]}"


def build_summary(values: dict[str, Any]) -> str:
    semantic = infer_semantic_labels(values)
    tissue = clean(values.get("tissue_or_material"))
    organism = semantic["organism"]
    primary = semantic["primary_factor"]
    secondary = semantic["secondary_factor"]
    primary_levels = [part.strip() for part in clean(values.get("primary_factor_levels")).split(",") if part.strip()]
    secondary_levels = [part.strip() for part in clean(values.get("secondary_factor_levels")).split(",") if part.strip()]
    comparisons = [part.strip() for part in clean(values.get("prespecified_comparisons_summary")).split(",") if part.strip()]
    question = clean(values.get("main_biological_question"))
    objective = clean(values.get("project_objective_sentence"))

    paragraphs: list[str] = []

    if tissue:
        paragraphs.append(
            f"The {tissue} is a biologically active tissue whose metabolic and inflammatory state is directly relevant to health and production in {organism or 'the study system'}. "
            f"Changes in {tissue} physiology can be reflected at the protein level, making proteomic profiling a useful approach for evaluating how nutritional and inflammatory factors influence that system."
        )

    if primary:
        if semantic["primary_detail"]:
            paragraphs.append(
                f"Dietary interventions are of particular interest when they are expected to modify inflammatory tone or related molecular pathways. "
                f"In the present study, {semantic['primary_detail']}, allowing assessment of whether the supplemented diet was associated with shifts in the {tissue} proteome. "
                f"Because the biological hypothesis motivating this study was that polyphenol supplementation may reduce inflammation, proteomic analysis provides a data-driven way to evaluate whether diet-associated protein abundance patterns are consistent with that expectation."
            )
        else:
            paragraphs.append(
                f"The primary design factor in this study was {primary}, evaluated across {oxford_join(primary_levels)}."
            )

    if secondary:
        if semantic["secondary_detail"]:
            paragraphs.append(
                f"Inflammatory challenge was examined by comparing {semantic['secondary_detail']}. "
                f"This comparison is biologically important because it helps distinguish proteomic changes associated with the inflammatory challenge itself from changes that may arise secondary to altered feed intake. "
                f"The factorial combination of {primary or 'the primary factor'} and {secondary} further supports evaluation of whether diet-associated proteomic effects are consistent across challenge contexts or differ between non-challenged and challenged animals."
            )
        else:
            paragraphs.append(
                f"A second factor, {secondary}, was evaluated across {oxford_join(secondary_levels)} so that both main effects and context-specific contrasts could be examined."
            )

    if comparisons:
        paragraphs.append(
            f"Untargeted LC-MS/MS proteomics provides a global view of protein abundance patterns in {tissue or 'the study tissue'} and can detect coordinated molecular changes associated with {primary or 'the primary factor'} and {secondary or 'the secondary factor'}. "
            f"In this study, proteomics was used to assess whether the {tissue or 'study'} protein profile differed across four prespecified contrasts: {oxford_join(comparisons)}."
        )

    if objective:
        paragraphs.append(objective.rstrip(".") + ".")
    elif question:
        paragraphs.append(f"The objective of this study was to evaluate {question}.")

    return "\n\n".join(paragraphs).strip() + "\n"


def main() -> int:
    args = parse_args()
    project_root = Path(args.project_root).resolve()
    values = load_json((project_root / args.values).resolve())
    project_context = load_json((project_root / args.project_context).resolve())
    merged = dict(values)
    for key, value in project_context.items():
        if value not in ("", None, [], {}):
            merged[key] = value
    doc_path = (project_root / args.input_doc).resolve()
    if not doc_path.exists():
        print(f"Skipping: missing {doc_path}")
        return 0

    text = doc_path.read_text(encoding="utf-8")
    text, bounds = ensure_section(text, "Manuscript-Style Summary")
    start, end = bounds
    refined = "\n\n" + build_summary(merged) + "\n"
    new_text = text[:start] + refined + text[end:]
    if new_text != text:
        doc_path.write_text(new_text, encoding="utf-8")
        print(f"Updated {doc_path}")
    else:
        print(f"No change to {doc_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
