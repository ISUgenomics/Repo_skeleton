# 02_Metadata

This file summarizes the finalized design recorded in [sample_metadata.csv](./workflow/00_raw_data/config/sample_metadata.csv) and [comparisons.csv](./workflow/00_raw_data/config/comparisons.csv).

<!-- Editor guide: use `✅` only after the project-specific metadata and comparisons have been validated in the completed run. -->

- [Design Summary](#design-summary)
  - [Sample Groups](#sample-groups)
  - [Required Metadata Columns](#required-metadata-columns)
- [Requested Comparisons](#requested-comparisons)
- [Validation Status](#validation-status)

## Design Summary

| Factor | Levels |
|---|---|
| `{{ factor_1_name }}` | `{{ factor_1_levels }}` |
| `{{ factor_2_name }}` | `{{ factor_2_levels }}` |
| `group` | `{{ full_groups }}` |

### Sample Groups

{{ sample_groups_table_md }}

⬜ All [`n={{ sample_count }}`] samples intended for the main run are represented after metadata finalization.  

### Required Metadata Columns

⬜ All required columns are present in [sample_metadata.csv](./workflow/00_raw_data/config/sample_metadata.csv):  

- `sample_id`
- `source_column`
- `{{ primary_grouping_column }}`
- `{{ secondary_grouping_column }}`
- `group`
- `replicate`
- `batch_or_run`
- `include`

The workflow-executed sample table is [workflow/01_qc_normalization/sample_metadata_used.csv](./workflow/01_qc_normalization/sample_metadata_used.csv).

## Requested Comparisons

Only these requested comparisons should be computed. Other possible combinations implied by the design should remain disabled unless they were explicitly requested for the project.

{{ requested_comparisons_table_md }}

## Validation Status

⬜ Every `source_column` in [sample_metadata.csv](./workflow/00_raw_data/config/sample_metadata.csv) matched a raw-data abundance column.  
⬜ Every `sample_id` is unique.  
⬜ All [`n={{ sample_count }}`] intended samples were retained for the main run, or exclusions are documented explicitly.  
⬜ All [`n={{ expected_group_count }}`] expected full treatment groups are represented in the metadata.  
⬜ Main-effect comparisons are supported by explicit columns [`{{ main_effect_columns }}`].  
⬜ Within-context or full-group comparisons are supported by the explicit column: [`group`].  
⬜ All [`n={{ requested_comparison_count }}`] requested comparisons are defined in [comparisons.csv](./workflow/00_raw_data/config/comparisons.csv) with explicit grouping columns and thresholds.  
⬜ The notebook used the config files rather than hardcoded sample lists.  
