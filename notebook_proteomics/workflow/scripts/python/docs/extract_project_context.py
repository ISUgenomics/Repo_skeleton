#!/usr/bin/env python3
"""Extract flat project-context fields from manifest, metadata, and text files."""

from __future__ import annotations

import argparse
import re
from datetime import date
from pathlib import Path

from common import parse_manifest_yaml, read_json, write_json


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--manifest-file", default="workflow/00_raw_data/config/project_manifest.yaml")
    parser.add_argument("--metadata-summary", default="workflow/scripts/python/docs/metadata_summary.json")
    parser.add_argument("--raw-data-dir", default="workflow/00_raw_data")
    parser.add_argument("--output-dir", default="workflow/scripts/python/docs")
    return parser.parse_args()


def read_text_contexts(raw_data_dir: Path) -> dict[str, str]:
    contexts: dict[str, str] = {}
    for path in sorted(raw_data_dir.glob("*.txt")):
        contexts[path.stem] = path.read_text().strip()
    return contexts


def token_key(text: str) -> str:
    return re.sub(r"[^a-z0-9]+", "_", text.lower()).strip("_")


def normalize_space(text: str) -> str:
    return " ".join(text.split())


def split_contacts(value: str) -> list[str]:
    if not value:
        return []
    if ";" in value:
        parts = value.split(";")
    else:
        parts = re.split(r"(?<=>)\s*,\s*(?=[^,]*<)", value)
    return [item.strip() for item in parts if item.strip()]


def contact_name(value: str) -> str:
    text = value.strip()
    if "<" in text:
        text = text.split("<", 1)[0].strip()
    text = re.sub(r"\[[^\]]+\]", "", text).strip()
    return normalize_space(text)


def contact_tag(value: str) -> str:
    match = re.search(r"\[([^\]]+)\]", value)
    return normalize_space(match.group(1)) if match else ""


def contact_affiliation(value: str) -> str:
    lower = value.lower()
    if "biotc" in lower:
        return "Bioinformatics Facility, Office of Biotechnology, Iowa State University"
    if "protein facility" in lower or "protein@" in lower:
        return "Protein Facility, Office of Biotechnology, Iowa State University"
    if "iastate.edu" in lower or "iowa state" in lower:
        return "Iowa State University"
    return ""


def parse_text_headers(text: str) -> dict[str, str]:
    headers = {"from": "", "date": "", "to": "", "cc": "", "subject": ""}
    for line in text.splitlines():
        stripped = line.strip()
        lower = stripped.lower()
        for key in list(headers):
            prefix = f"{key}:"
            if lower.startswith(prefix):
                headers[key] = stripped.split(":", 1)[1].strip()
    return headers


def parse_context_sections(text_contexts: dict[str, str]) -> dict[str, list[str]]:
    heading_map = {
        "authors": "authors",
        "author": "authors",
        "affiliations": "affiliations",
        "affiliation": "affiliations",
        "contributions": "contributions",
        "contribution": "contributions",
        "funding": "funding",
        "acknowledgements": "acknowledgements",
        "acknowledgments": "acknowledgements",
        "acknowledgement": "acknowledgements",
        "acknowledgment": "acknowledgements",
        "system or tissue references": "system_refs",
        "system references": "system_refs",
        "tissue references": "system_refs",
        "condition or treatment references": "condition_refs",
        "condition references": "condition_refs",
        "treatment references": "condition_refs",
        "project-specific references": "project_refs",
        "project specific references": "project_refs",
        "local relevant references": "local_refs",
        "local references": "local_refs",
        "references": "generic_refs",
    }
    sections: dict[str, list[str]] = {value: [] for value in set(heading_map.values())}
    for text in text_contexts.values():
        current = ""
        for raw in text.splitlines():
            line = raw.strip()
            if not line:
                continue
            lowered = line.lower().rstrip(":")
            if lowered in heading_map:
                current = heading_map[lowered]
                continue
            if re.match(r"^(Date|From|To|Cc|Subject):", line, flags=re.IGNORECASE):
                continue
            item = re.sub(r"^[-*•]\s*", "", line).strip()
            if current and item:
                sections[current].append(item)
    return sections


def parse_correspondence(text: str) -> dict[str, str]:
    headers = parse_text_headers(text)
    excerpt_lines: list[str] = []
    for line in text.splitlines():
        stripped = line.strip()
        if re.match(r"^(Date|From|To|Cc|Subject):", stripped, flags=re.IGNORECASE):
            continue
        if stripped:
            excerpt_lines.append(stripped)
    excerpt = "\n\n".join(excerpt_lines).strip()
    return {
        "key_correspondence_date": headers["date"],
        "key_correspondence_sender": headers["from"],
        "key_correspondence_to": headers["to"],
        "key_correspondence_cc": headers["cc"],
        "key_correspondence_subject": headers["subject"],
        "key_correspondence_excerpt": excerpt,
    }


def raw_data_format_from_manifest(manifest: dict) -> str:
    fmt = str(manifest.get("analysis", {}).get("input_format", "")).lower()
    mapping = {
        "xlsx": "grouped abundance Excel file",
        "xls": "grouped abundance Excel file",
        "csv": "comma-separated abundance table",
        "tsv": "tab-delimited abundance table",
        "txt": "text abundance table",
    }
    return mapping.get(fmt, fmt)


def platform_from_context(texts: dict[str, str]) -> str:
    combined = "\n".join(texts.values())
    if "untargeted LC-MS/MS proteomics" in combined:
        return "untargeted LC-MS/MS proteomics"
    if "LC-MS/MS proteomics" in combined:
        return "LC-MS/MS proteomics"
    return "proteomics"


def count_rows_for_value(rows: list[dict], column: str, value: str) -> int:
    if not column or not value:
        return 0
    return sum(1 for row in rows if row.get(column, "") == value)


def infer_team_fields(text_contexts: dict[str, str]) -> dict[str, str]:
    parsed_headers = [parse_text_headers(text) for text in text_contexts.values()]
    from_values = [item["from"] for item in parsed_headers if item.get("from")]
    to_values = [item["to"] for item in parsed_headers if item.get("to")]
    cc_values = [item["cc"] for item in parsed_headers if item.get("cc")]
    subjects = [item["subject"] for item in parsed_headers if item.get("subject")]
    combined = "\n".join(text_contexts.values())

    sender = from_values[0] if from_values else ""
    to_contacts = split_contacts(to_values[0]) if to_values else []
    cc_contacts = split_contacts(cc_values[0]) if cc_values else []
    subject = subjects[0] if subjects else ""

    principal_investigator = contact_name(sender)
    primary_contact = sender or principal_investigator
    project_contact = to_contacts[0] if to_contacts else ""
    analysis_group = ""
    data_source = ""
    analysis_lead = ""

    for contact in to_contacts + cc_contacts:
        lower = contact.lower()
        if not analysis_group and ("biotc" in lower or "bioinformatics" in lower):
            analysis_group = contact_tag(contact) or contact_name(contact)
        if not data_source and ("protein facility" in lower or "protein@" in lower):
            data_source = contact_name(contact)

    lead_match = re.search(r"(?:have|let(?:’|')s have)\s+([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)\s+take lead", combined)
    if lead_match:
        analysis_lead = normalize_space(lead_match.group(1))

    contact_match = re.search(r"main contact for\s+([A-Z][a-z]+)", combined)
    if contact_match and not project_contact and to_contacts:
        project_contact = to_contacts[0]

    if not analysis_group and to_contacts:
        analysis_group = contact_name(to_contacts[0])
    if not data_source and cc_contacts:
        data_source = contact_name(cc_contacts[0])

    return {
        "principal_investigator": principal_investigator,
        "primary_contact": primary_contact,
        "project_contact": contact_name(project_contact) if project_contact else primary_contact,
        "analysis_group_or_facility": analysis_group,
        "analysis_lead": analysis_lead,
        "data_source_or_facility": data_source,
        "correspondence_subject": subject,
    }


def first_nonempty(*values: str) -> str:
    for value in values:
        if value:
            return value
    return ""


def infer_manuscript_support_fields(text_contexts: dict[str, str], team_fields: dict[str, str]) -> dict[str, str]:
    sections = parse_context_sections(text_contexts)
    payload: dict[str, str] = {"validation_date": str(date.today())}

    authors = sections.get("authors", [])
    affiliations = sections.get("affiliations", [])
    contributions = sections.get("contributions", [])

    inferred_authors = [
        team_fields.get("principal_investigator", ""),
        team_fields.get("analysis_lead", ""),
        team_fields.get("project_contact", ""),
    ]
    inferred_affiliations = [
        first_nonempty(contact_affiliation(team_fields.get("primary_contact", "")), "Iowa State University"),
        first_nonempty(team_fields.get("analysis_group_or_facility", ""), "Iowa State University"),
        first_nonempty(contact_affiliation(team_fields.get("project_contact", "")), team_fields.get("analysis_group_or_facility", "")),
    ]
    inferred_contributions = [
        "Project lead",
        "Analysis lead",
        "Project contact or review support",
    ]

    for idx in range(1, 4):
        payload[f"author_{idx}"] = authors[idx - 1] if len(authors) >= idx else inferred_authors[idx - 1]
        payload[f"affiliation_{idx}"] = affiliations[idx - 1] if len(affiliations) >= idx else inferred_affiliations[idx - 1]
        payload[f"contribution_{idx}"] = contributions[idx - 1] if len(contributions) >= idx else inferred_contributions[idx - 1]

    funding_lines = sections.get("funding", [])
    ack_lines = sections.get("acknowledgements", [])
    generic_refs = sections.get("generic_refs", [])
    system_refs = sections.get("system_refs", [])
    condition_refs = sections.get("condition_refs", [])
    project_refs = sections.get("project_refs", [])
    local_refs = sections.get("local_refs", [])

    payload["funding_statement"] = " ".join(funding_lines[:3]).strip()
    if ack_lines:
        payload["acknowledgement_statement"] = " ".join(ack_lines[:3]).strip()
    else:
        parts = []
        if team_fields.get("data_source_or_facility"):
            parts.append(team_fields["data_source_or_facility"])
        if team_fields.get("analysis_group_or_facility"):
            parts.append(team_fields["analysis_group_or_facility"])
        if parts:
            payload["acknowledgement_statement"] = "We acknowledge " + " and ".join(parts) + " for project support."

    if generic_refs:
        if not system_refs:
            system_refs = generic_refs[:3]
        if len(generic_refs) > 3 and not condition_refs:
            condition_refs = generic_refs[3:6]
        if len(generic_refs) > 6 and not project_refs:
            project_refs = generic_refs[6:9]

    for idx in range(1, 4):
        payload[f"system_or_tissue_reference_{idx}"] = system_refs[idx - 1] if len(system_refs) >= idx else ""
        payload[f"condition_or_treatment_reference_{idx}"] = condition_refs[idx - 1] if len(condition_refs) >= idx else ""
        payload[f"project_specific_reference_{idx}"] = project_refs[idx - 1] if len(project_refs) >= idx else ""
    for idx in range(1, 3):
        payload[f"local_relevant_reference_{idx}"] = local_refs[idx - 1] if len(local_refs) >= idx else ""

    return payload


def main() -> None:
    args = parse_args()
    manifest = parse_manifest_yaml(Path(args.manifest_file).resolve())
    metadata_summary = read_json(Path(args.metadata_summary).resolve()) or {}
    raw_data_dir = Path(args.raw_data_dir).resolve()
    output_dir = Path(args.output_dir).resolve()

    text_contexts = read_text_contexts(raw_data_dir)
    correspondence = parse_correspondence(text_contexts.get("correspondence", ""))
    team_fields = infer_team_fields(text_contexts)
    manuscript_fields = infer_manuscript_support_fields(text_contexts, team_fields)

    factor_columns = metadata_summary.get("factor_columns", [])
    factor_levels = metadata_summary.get("factor_levels", {})
    groups = metadata_summary.get("groups", [])
    comparisons = metadata_summary.get("comparisons", [])
    rows = metadata_summary.get("rows", [])

    primary_factor = factor_columns[0] if len(factor_columns) > 0 else ""
    secondary_factor = factor_columns[1] if len(factor_columns) > 1 else ""
    primary_levels = factor_levels.get(primary_factor, [])
    secondary_levels = factor_levels.get(secondary_factor, [])

    payload = {
        "project_title": manifest.get("project", {}).get("project_title", ""),
        "tissue_or_material": manifest.get("project", {}).get("material", ""),
        "platform": platform_from_context(text_contexts),
        "raw_data_format": raw_data_format_from_manifest(manifest),
        "conditions_or_groups": ", ".join(group.get("group", "") for group in groups),
        "full_groups": ", ".join(group.get("group", "") for group in groups),
        "group_size": ", ".join(f"{group.get('group', '')} (n={group.get('count', 0)})" for group in groups),
        "one_sentence_summary": (
            f"This project analyzes {metadata_summary.get('sample_count', '')} "
            f"{manifest.get('project', {}).get('material', '')} samples from "
            f"{manifest.get('project', {}).get('organism', '')}."
        ).strip(),
        "main_biological_question": (
            f"whether {primary_factor} and {secondary_factor} alter the "
            f"{manifest.get('project', {}).get('material', '')} proteome of "
            f"{manifest.get('project', {}).get('organism', '')}"
        ).strip(),
        "biological_question": (
            f"Whether {primary_factor} and {secondary_factor} alter the "
            f"{manifest.get('project', {}).get('material', '')} proteome of "
            f"{manifest.get('project', {}).get('organism', '')}."
        ).strip(),
        "primary_group_1": primary_levels[0] if len(primary_levels) > 0 else "",
        "primary_group_2": primary_levels[1] if len(primary_levels) > 1 else "",
        "secondary_group_1": secondary_levels[0] if len(secondary_levels) > 0 else "",
        "secondary_group_2": secondary_levels[1] if len(secondary_levels) > 1 else "",
        "primary_group_labels_note": "Primary and secondary labels reflect the main experimental factors.",
        "primary_hypothesis": (
            f"{primary_factor} and {secondary_factor} change the "
            f"{manifest.get('project', {}).get('material', '')} proteome"
        ).strip(),
        "secondary_hypothesis": f"{primary_factor} produces a measurable main-effect proteomic shift" if primary_factor else "",
        "tertiary_hypothesis": f"{secondary_factor} produces a measurable main-effect proteomic shift" if secondary_factor else "",
        "quaternary_hypothesis": f"the effect of {primary_factor} depends on {secondary_factor}" if primary_factor and secondary_factor else "",
        "factor_1_name": primary_factor,
        "factor_1_levels": ", ".join(primary_levels),
        "factor_2_name": secondary_factor,
        "factor_2_levels": ", ".join(secondary_levels),
        "primary_factor_name": primary_factor,
        "primary_factor_levels": ", ".join(primary_levels),
        "secondary_factor_name": secondary_factor,
        "main_effect_columns": ", ".join([col for col in factor_columns[:2] if col]),
        "expected_group_count": str(len(groups)),
        "primary_grouping_column": primary_factor,
        "secondary_grouping_column": secondary_factor,
        "requested_comparison_count": str(len(comparisons)),
        "requested_comparison_scope": ", ".join(comp.get("comparison_id", "") for comp in comparisons),
        "primary_factor_name_and_levels": f"{primary_factor}: {', '.join(primary_levels)}" if primary_factor else "",
        "secondary_factor_name_and_levels": f"{secondary_factor}: {', '.join(secondary_levels)}" if secondary_factor else "",
        "design_note": "The study uses a factorial design with separate main-effect and context-specific comparisons.",
        "input_format": str(manifest.get("analysis", {}).get("input_format", "")),
        "upper_quartile_normalization": "true" if str(manifest.get("analysis", {}).get("apply_uq_per_comparison", "")).lower() == "true" else "false",
        "qvalue_plots": "true" if str(manifest.get("analysis", {}).get("generate_qvalue_plots", "")).lower() == "true" else "false",
        "zero_handling_description": "Zeros are treated according to the configured astral_mode setting during statistical filtering.",
        "raw_data_notes": "Primary raw data file used for the completed workflow run.",
        "metadata_source_notes": "Project-provided metadata reference file used to prepare or validate sample metadata.",
        "visible_only_copy_status": "not used",
        "main_experimental_factors": f"{primary_factor} and {secondary_factor}".strip(" and "),
        "main_factors": f"{primary_factor} and {secondary_factor}".strip(" and "),
        "prespecified_comparisons_summary": ", ".join(comp.get("comparison_id", "") for comp in comparisons),
        "primary_biological_hypothesis": (
            f"{primary_factor} and {secondary_factor} change the {manifest.get('project', {}).get('material', '')} proteome"
        ).strip(),
        "primary_factor_question": f"whether {primary_factor} alters the proteome" if primary_factor else "",
        "primary_factor_rationale": f"{primary_factor} is one of the main experimental factors in this study." if primary_factor else "",
        "secondary_factor_levels_and_rationale": (
            f"{secondary_factor}: {', '.join(secondary_levels)}; this factor provides the main challenge or context contrast."
            if secondary_factor else ""
        ),
        "secondary_factor_effect": f"whether {secondary_factor} alters the proteome" if secondary_factor else "",
        "confounding_or_context_factor": secondary_factor,
        "interaction_or_context_question": (
            f"whether the effect of {primary_factor} depends on {secondary_factor}" if primary_factor and secondary_factor else ""
        ),
        "project_objective_sentence": (
            f"The objective of this study was to characterize proteomic differences across the prespecified contrasts: "
            f"{', '.join(comp.get('comparison_id', '') for comp in comparisons)}."
        ),
        "biological_relevance": (
            f"{manifest.get('project', {}).get('material', '').capitalize()} provides the biological context for this proteomics study."
        ),
        **team_fields,
        **manuscript_fields,
        **correspondence,
    }

    payload["text_context_file_count"] = str(len(text_contexts))
    payload["text_context_files"] = ", ".join(f"{stem}.txt" for stem in sorted(text_contexts))
    for stem, text in text_contexts.items():
        payload[f"text_context_{token_key(stem)}"] = text

    for idx, group in enumerate(groups[:4], start=1):
        payload[f"group_{idx}"] = group.get("group", "")
        payload[f"group_{idx}_count"] = str(group.get("count", ""))
        payload[f"group_{idx}_sample_ids"] = ", ".join(group.get("sample_ids", []))

    for idx, comp in enumerate(comparisons[:4], start=1):
        payload[f"comparison_{idx}"] = comp.get("comparison_id", "")
        payload[f"comparison_{idx}_label"] = comp.get("comparison_id", "")
        grouping = comp.get("grouping_column", "")
        if grouping == primary_factor and primary_factor:
            interpretation = f"main {primary_factor} effect"
        elif grouping == secondary_factor and secondary_factor:
            interpretation = f"main {secondary_factor} effect"
        elif grouping == "group" and primary_factor and secondary_factor:
            interpretation = f"context-specific {primary_factor} effect within {secondary_factor}"
        else:
            interpretation = f"{grouping} comparison" if grouping else "requested comparison"
        payload[f"comparison_{idx}_interpretation"] = interpretation
        if grouping == "group":
            group_size = next((g.get("count", 0) for g in groups if g.get("group") == comp.get("group1")), 0)
        else:
            group_size = count_rows_for_value(rows, grouping, comp.get("group1", ""))
        payload[f"comparison_{idx}_group_size"] = f"n={group_size} per group" if group_size else ""

    for stem, text in text_contexts.items():
        if stem == "summary":
            payload["one_sentence_summary"] = " ".join(text.split())
        elif stem == "biological_question":
            payload["biological_question"] = " ".join(text.split())
            payload["main_biological_question"] = " ".join(text.split())

    write_json(output_dir / "project_context.json", payload)
    print(f"Wrote {output_dir / 'project_context.json'}")


if __name__ == "__main__":
    main()
