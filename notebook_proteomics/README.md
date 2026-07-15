<!-- Editor guide
Use this file as the short landing page for the copied project.

- Replace unresolved variables with project-specific facts.
- Keep this file shorter than [00_Background.md](./00_Background.md).
- Keep biological rationale high-level here; detailed workflow facts belong in `workflow/`.
- Use `✅` only after the project-specific run has been completed and validated.
-->
# {{ project_title }}

{{ one_sentence_summary }}

This project analyzes proteomics data from `{{ organism_or_system }}` using `{{ sample_count }}` samples collected from `{{ tissue_or_material }}`. The study compares `{{ conditions_or_groups }}` to address `{{ main_biological_question }}`.

Experimental design was:

| **primary groups:** | **secondary groups:** |
|---|---|
| `{{ primary_group_1 }}` | `{{ secondary_group_1 }}` |
| `{{ primary_group_2 }}` | `{{ secondary_group_2 }}` |

*`{{ primary_group_labels_note }}`*

## Biological Question

{{ biological_question }}

## Hypotheses

**Whether `{{ primary_hypothesis }}`.**

*The proteomic evidence that would support or contextualize that biological effect, include:*
- Whether `{{ secondary_hypothesis }}`.
- Whether `{{ tertiary_hypothesis }}`.
- Whether `{{ quaternary_hypothesis }}`.

## Expected Comparisons

| Comparison | Interpretation | Group size |
|---|---|---|
| `{{ comparison_1 }}` | `{{ comparison_1_interpretation }}` | `{{ comparison_1_group_size }}` |
| `{{ comparison_2 }}` | `{{ comparison_2_interpretation }}` | `{{ comparison_2_group_size }}` |
| `{{ comparison_3 }}` | `{{ comparison_3_interpretation }}` | `{{ comparison_3_group_size }}` |
| `{{ comparison_4 }}` | `{{ comparison_4_interpretation }}` | `{{ comparison_4_group_size }}` |

## Publication-Level Notes

The root numbered markdown files (`*.md`) record the project design, file inventory, metadata decisions, methods, and result summaries in a format that can be adapted directly in manuscript writing.

| Area | File |
|---|---|
| Background and study scope | [00_Background.md](./00_Background.md) |
| Inputs and outputs | [01_Files.md](./01_Files.md) |
| Sample design and comparisons | [02_Metadata.md](./02_Metadata.md) |
| Experimental and computational methods | [03_Methods.md](./03_Methods.md) |
| Current results summary | [**04_Results.md**](./04_Results.md) |
| Scientific Introduction | [05_Introduction.md](./05_Introduction.md) |

## Analysis Status

⬜ Raw input data file validated: [{{ raw_data_file }}](./workflow/00_raw_data/)
⬜ Metadata source file validated: [{{ metadata_source_file }}](./workflow/00_raw_data/)
⬜ Final sample metadata file prepared: [sample_metadata.csv](./workflow/00_raw_data/config/sample_metadata.csv)
⬜ Final comparison file prepared: [comparisons.csv](./workflow/00_raw_data/config/comparisons.csv)
⬜ Main [notebook run](./workflow/scripts/notebooks/proteomics_analysis.ipynb) completed and outputs were written in [**workflow/**](./workflow/)

Documentation from workflow execution: [**Final report**](./workflow/final_report/README.md)

| Area | File |
|---|---|
| Raw-data intake notes | [workflow/00_raw_data/README.md](./workflow/00_raw_data/README.md) |
| Workflow config files | [workflow/00_raw_data/config/README.md](./workflow/00_raw_data/config/README.md) |
| QC and normalization outputs | [workflow/01_qc_normalization/README.md](./workflow/01_qc_normalization/README.md) |
| Statistics outputs | [workflow/02_statistics/README.md](./workflow/02_statistics/README.md) |
| Visualization outputs | [workflow/03_visualization/README.md](./workflow/03_visualization/README.md) |
| Script and notebook entry points | [workflow/scripts/README.md](./workflow/scripts/README.md) |
