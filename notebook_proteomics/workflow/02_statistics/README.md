<!--
Editor notes:
- Document the actual comparisons run, the commands or notebook sections used, the result tables generated, and any deviations from the planned comparison set.
- The visible report should read like a completed run log, not a to-do list.
-->
# 02_statistics

Statistical analysis outputs.

*This step documents the differential abundance comparisons run for the project and the result tables generated from the normalized proteomics matrix. It records which comparisons were tested, which thresholds were applied, and where the main statistical signal was observed.*

## Input Files

Input files used for statistical testing:

| File | Purpose |
|------|---------|
| [`../00_raw_data/config/sample_metadata.csv`](../00_raw_data/config/sample_metadata.csv) | treatment groups and sample annotations |
| [`../00_raw_data/config/comparisons.csv`](../00_raw_data/config/comparisons.csv) | enabled comparisons and thresholds |
| [`../01_qc_normalization/normalized_abundance_matrix.csv`](../01_qc_normalization/normalized_abundance_matrix.csv) | normalized matrix from [01_qc_normalization](../01_qc_normalization/README.md) |

## Comparison Summary

Comparisons tested in this project:
- ⬜ primary comparison set completed as defined in [`../00_raw_data/config/comparisons.csv`](../00_raw_data/config/comparisons.csv)
- ⬜ one or more configured comparisons were skipped
- ⬜ one or more additional comparisons were added during analysis

Statistical settings used in this step:

| Item | Value |
|------|-------|
| Statistical test or model | `Student's t-test with per-group Shapiro-Wilk normality reporting and fold-change calculation` |
| Grouping variable used for comparisons | `{{ grouping_columns_used }}` |
| Multiple-testing correction method | `Benjamini-Hochberg FDR` |
| Significance thresholds | `p < 0.05`, `q < 0.05`, `abs(log2FC) > 1` |

{{ comparison_overview_table_md }}

## Execution

This step was run from the `# Run statistics and generate plots` section of [`proteomics_analysis.ipynb`](../scripts/notebooks/proteomics_analysis.ipynb), using the shared statistical functions in [`Stats.py`](../scripts/python/Stats.py).

All enabled comparison tables were generated successfully. Summary hit counts are recorded above and in [`significant_protein_counts.csv`](./significant_protein_counts.csv).

### Number of significantly DE proteins

{{ significant_hit_count_table_md }}

## Output Files

Statistical result files generated in this step:

| Name | Description |
|------|-------------|
| [`CSV/`](./CSV) | per-comparison statistics tables |
| [`significant_protein_counts.csv`](./significant_protein_counts.csv) | summary table of significant proteins across comparisons |

## Status & Notes

STATUS: `{{ statistics_status }}`

- Deviations from planned comparisons in [`../00_raw_data/config/comparisons.csv`](../00_raw_data/config/comparisons.csv): `{{ comparison_deviations }}` 
- Statistical method or threshold changes applied during the run: `{{ statistical_method_changes }}` 
- Any caveat that should be carried into [04_Results.md](../../04_Results.md): `{{ carry_forward_statistics_note }}`
