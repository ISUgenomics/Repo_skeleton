# 00_Background

This file records the project context, study scope, team, and key request details that define why the analysis was performed.

- [Project Overview](#project-overview)
- [Research Team](#research-team)
- [Experimental Design](#experimental-design)
- [Project Goals](#project-goals)
- [Key Project Decisions](#key-project-decisions)
  - [Key Correspondence](#key-correspondence)

## Project Overview

This project evaluates whether `{{ main_biological_question }}` alters the `{{ tissue_or_material }}` proteome of `{{ organism_or_system }}`. The study uses `{{ platform }}` on `{{ sample_count }}` samples collected from `{{ tissue_or_material }}`.

The experimental design is:

- primary factor: `{{ primary_factor_name_and_levels }}`
- secondary factor: `{{ secondary_factor_name_and_levels }}`
- full groups: `{{ full_groups }}`
- group size: `{{ group_size }}`

## Research Team

- **Principal Investigator:** `{{ principal_investigator }}`
  - primary contact: `{{ primary_contact }}`
- data source: `{{ data_source_or_facility }}`
- data analysis: `{{ analysis_group_or_facility }}`
  - analysis lead: `{{ analysis_lead }}`
  - project contact: `{{ project_contact }}`

## Experimental Design

| Attribute | Value |
|---|---|
| Organism | `{{ organism_or_system }}` |
| Tissue or material | `{{ tissue_or_material }}` |
| Samples | `{{ sample_count }}` |
| Platform | `{{ platform }}` |
| Raw data format | `{{ raw_data_format }}` |

**Study design summary:**

| **primary groups:** | **secondary groups:** |
|---|---|
| `{{ primary_group_1 }}` | `{{ secondary_group_1 }}` |
| `{{ primary_group_2 }}` | `{{ secondary_group_2 }}` |

- `{{ design_note }}`

The planned comparisons are summarized in [02_Metadata.md](./02_Metadata.md), and the executed workflow is described in [03_Methods.md](./03_Methods.md).

## Project Goals

1. Perform a standard proteomics analysis for the study design and return interpretable comparison-level results.
   - confirm that the [supplied raw data](./workflow/00_raw_data/) and any metadata source file are suitable for the workflow
   - prepare and validate [sample_metadata.csv](./workflow/00_raw_data/config/sample_metadata.csv) and [comparisons.csv](./workflow/00_raw_data/config/comparisons.csv)
   - run the [proteomics workflow](./workflow/scripts/notebooks/proteomics_analysis.ipynb): filtering, normalization, statistical testing, and standard proteomics visualizations
   - summarize results for the requested contrasts only
2. Create project documentation that can support follow-up interpretation and manuscript drafting.

## Key Project Decisions

- Use `{{ raw_data_file }}` as the primary raw-data input file.
- Limit enabled comparisons to `{{ requested_comparison_scope }}`.

### Key Correspondence

**Date:** `{{ key_correspondence_date }}`  
**From:** `{{ key_correspondence_sender }}`

```text
{{ key_correspondence_excerpt }}
```
