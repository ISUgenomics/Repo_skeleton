<!--
Editor notes:
- Use this file as the canonical workflow run summary for the project.
- Keep it concise, structured, and easy to parse by a human or script.
- Prefer exact values and status tables over narrative paragraphs.
-->
# final_report

*This file is the canonical workflow run summary. It summarizes step completion, final settings, key outputs, and carry-forward caveats for reuse in the root project docs.*

## Workflow Status

main notebook run completed: `{{ final_run_status }}`

| Status | Step | Description | Primary output | Notes |
|---|---|---|---|---|
| `{{ raw_data_step_status }}` | [00_raw_data](../00_raw_data/README.md) | primary raw data file validation | `{{ raw_data_primary_output }}` | `{{ raw_data_step_note }}` |
| `{{ qc_step_status }}` | [01_qc_normalization](../01_qc_normalization/README.md) | filtering, metadata alignment, and primary normalization | [normalized_abundance_matrix.csv](../01_qc_normalization/normalized_abundance_matrix.csv) | `{{ qc_step_note }}` |
| `{{ statistics_step_status }}` | [02_statistics](../02_statistics/README.md) | comparison-level statistical testing and hit counting | [significant_protein_counts.csv](../02_statistics/significant_protein_counts.csv) | `{{ statistics_step_note }}` |
| `{{ visualization_step_status }}` | [03_visualization](../03_visualization/README.md) | figure generation in static and interactive formats | [output/](../03_visualization/output/) | `{{ visualization_step_note }}` |
| `{{ secondary_step_status }}` | [04_secondary_analyses](../04_secondary_analyses/README.md) | optional follow-up comparisons or remake steps | `{{ secondary_primary_output_or_none }}` | `{{ secondary_step_note }}` |

## Final Settings Used

| Setting | Value |
|---|---|
| raw data file | [`{{ raw_data_file }}`](../00_raw_data/) |
| metadata source | [`{{ metadata_source_file }}`](../00_raw_data/) |
| sample metadata | [`workflow/00_raw_data/config/sample_metadata.csv`](../00_raw_data/config/sample_metadata.csv) |
| comparisons file | [`workflow/00_raw_data/config/comparisons.csv`](../00_raw_data/config/comparisons.csv) |
| samples retained | `{{ sample_count }}` |
| enabled comparisons | `{{ enabled_comparison_count }}` |
| PSM threshold | `> {{ psm_threshold }}` |
| abundance column pattern | `{{ abundance_column_pattern }}` |
| primary normalization | `{{ primary_normalization }}` |
| per-comparison upper-quartile normalization | `{{ upper_quartile_normalization }}` |
| `astral_mode` | `{{ astral_mode }}` |
| p-value cutoff | `0.05` |
| q-value cutoff | `0.05` |
| abs(log2FC) cutoff | `> 1` |
| q-value plots generated | `{{ qvalue_plots }}` |
| software versions | [`software_versions.txt`](../01_qc_normalization/software_versions.txt) |

## Issues and Resolutions

| Issue | Resolution | Impact on run |
|---|---|---|
| `{{ issue_or_none }}` | `{{ issue_resolution }}` | `{{ issue_impact }}` |

## Key Outputs

| Output | File or folder |
|---|---|
| normalized matrix | [normalized_abundance_matrix.csv](../01_qc_normalization/normalized_abundance_matrix.csv) |
| annotation table | [annotation.csv](../01_qc_normalization/annotation.csv) |
| comparison summary | [significant_protein_counts.csv](../02_statistics/significant_protein_counts.csv) |
| comparison CSVs | [CSV/](../02_statistics/CSV/) |
| static plots | [PNG](../03_visualization/output/PNG) |
| vector plots | [SVG](../03_visualization/output/SVG) |
| interactive plots | [HTML](../03_visualization/output/HTML) |
| extracted hit summary | [significant_hits_summary.json](../scripts/python/docs/significant_hits_summary.json) |
| report-ready results | [../../04_Results.md](../../04_Results.md) |

## Carry-Forward Notes

- `{{ carry_forward_note_1 }}`
- `{{ carry_forward_note_2 }}`
- `{{ carry_forward_note_3 }}`
