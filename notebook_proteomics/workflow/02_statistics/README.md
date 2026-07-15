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
⬜ primary comparison set completed as defined in [`../00_raw_data/config/comparisons.csv`](../00_raw_data/config/comparisons.csv)
⬜ one or more configured comparisons were skipped
⬜ one or more additional comparisons were added during analysis

Statistical settings used in this step:

| Item | Value |
|------|-------|
| Statistical test or model | `Student's t-test with per-group Shapiro-Wilk normality reporting and fold-change calculation` |
| Grouping variable used for comparisons | `{{ grouping_columns_used }}` |
| Multiple-testing correction method | `Benjamini-Hochberg FDR` |
| Significance thresholds | `p < 0.05`, `q < 0.05`, `abs(log2FC) > 1` |

| comparison_id | group1 | group2 | p-value cutoff | q-value cutoff | abs_log2fc cutoff | output file |
|---------------|--------|--------|----------------|----------------|-------------------|-------------|
| `{{ comparison_1_id }}` | `{{ comparison_1_group1 }}` | `{{ comparison_1_group2 }}` | `0.05` | `0.05` | `1` | [`CSV/{{ comparison_1_output_file }}`](./CSV/) |
| `{{ comparison_2_id }}` | `{{ comparison_2_group1 }}` | `{{ comparison_2_group2 }}` | `0.05` | `0.05` | `1` | [`CSV/{{ comparison_2_output_file }}`](./CSV/) |
| `{{ comparison_3_id }}` | `{{ comparison_3_group1 }}` | `{{ comparison_3_group2 }}` | `0.05` | `0.05` | `1` | [`CSV/{{ comparison_3_output_file }}`](./CSV/) |
| `{{ comparison_4_id }}` | `{{ comparison_4_group1 }}` | `{{ comparison_4_group2 }}` | `0.05` | `0.05` | `1` | [`CSV/{{ comparison_4_output_file }}`](./CSV/) |

## Execution

This step was run from the `# Run statistics and generate plots` section of [`proteomics_analysis.ipynb`](../scripts/notebooks/proteomics_analysis.ipynb), using the shared statistical functions in [`Stats.py`](../scripts/python/Stats.py).

All enabled comparison tables were generated successfully. Summary hit counts are recorded above and in [`significant_protein_counts.csv`](./significant_protein_counts.csv).

### Number of significantly DE proteins

| Comparison | Proteins with significant pvalue | Proteins with significant qvalue |
| -- | -- | -- |
| `{{ comparison_1_label }}` | `{{ comparison_1_p_hits }}` | `{{ comparison_1_q_hits }}` |
| `{{ comparison_2_label }}` | `{{ comparison_2_p_hits }}` | `{{ comparison_2_q_hits }}` |
| `{{ comparison_3_label }}` | `{{ comparison_3_p_hits }}` | `{{ comparison_3_q_hits }}` |
| `{{ comparison_4_label }}` | `{{ comparison_4_p_hits }}` | `{{ comparison_4_q_hits }}` |

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
