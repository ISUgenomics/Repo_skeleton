<!-- Editor notes:
- Start this file by documenting the exact source files used for the project.
- Keep visible content factual and tied to the actual input files used in the run.
- If no preprocessing was needed, keep that explicit rather than leaving the section ambiguous.
- Use `✅` only after the project-specific intake review has been completed and validated.
-->
# 00_raw_data

Raw data and project intake record.

*This step documents the source files and starting data used for the proteomics analysis. It captures what was received, what was cleaned or retained, and which project-specific inputs were carried into the downstream workflow.*

## Input Files

| Item | Value |
|------|-------|
| Raw data file | [{{ raw_data_file }}](./{{ raw_data_file }}) |
| Original format | `{{ raw_data_format }}` |
| Raw data location | `workflow/00_raw_data/` |
| Project manifest used for this run | [`config/project_manifest.yaml`](./config/project_manifest.yaml) |
| Sample metadata used for this run | [`config/sample_metadata.csv`](./config/sample_metadata.csv) |
| Comparison definitions used for this run | [`config/comparisons.csv`](./config/comparisons.csv) |
| Cleaned export used for analysis | `{{ cleaned_export_used }}` |

## Notes

Data intake notes for this project:

The raw intake files for this project consisted of `{{ received_files }}`. The starting dataset for the main workflow was `{{ main_input_file }}`, used `{{ provided_or_after_preprocessing }}`.

- Hidden rows present: `{{ hidden_rows_present }}`
- Hidden columns present: `{{ hidden_columns_present }}`
- Visible-only export used: `{{ visible_only_used }}`
- Sample naming matched [`config/sample_metadata.csv`](./config/sample_metadata.csv): `{{ sample_naming_match_status }}`
- Comparison groups required for [`config/comparisons.csv`](./config/comparisons.csv) were present in the source data: `{{ comparison_group_presence_status }}`

## Optional Preprocessing

Preprocessing applied before the main proteomics workflow:

| Done | Step | Notes |
|------|------|-------|
| `⬜` | No preprocessing required | `{{ preprocessing_note_none }}` |
| `⬜` | Visible-only export created | `{{ preprocessing_note_visible_only }}` |
| `⬜` | Sample names standardized | `{{ preprocessing_note_sample_names }}` |
| `⬜` | Annotation fields standardized | `{{ preprocessing_note_annotations }}` |
| `⬜` | Abundance or identifier columns renamed | `{{ preprocessing_note_column_renames }}` |
| `⬜` | Non-data rows removed | `{{ preprocessing_note_removed_rows }}` |

## Execution

Commands or manual actions used during intake and preprocessing:

⬜ confirmed that `{{ main_input_file }}` contains the expected abundance columns plus protein metadata fields  
⬜ confirmed that `{{ visible_only_decision }}`  

## Final File Passed to Analysis

Final file passed to [01_qc_normalization](../01_qc_normalization/README.md): [{{ final_analysis_input }}](./{{ final_analysis_input }})
