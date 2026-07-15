<!--
Editor notes:
- Record the actual QC decisions, normalization method, exclusions, commands, and output files produced in this step.
- Keep the visible text focused on what was done and what was observed.
-->
# 01_qc_normalization

Quality control and normalization summary.

*This step documents how the protein abundance matrix was reviewed and prepared before statistical testing. It captures the QC filters, normalization choices, and any sample- or feature-level decisions that affect downstream differential abundance results.*

## Input Files

| File | Purpose |
|------|---------|
| [`../00_raw_data/{{ raw_data_file }}`](../00_raw_data/) | raw grouped-abundance matrix from [00_raw_data](../00_raw_data/README.md) |
| [`../00_raw_data/config/sample_metadata.csv`](../00_raw_data/config/sample_metadata.csv) | sample metadata and grouping |
| [`../00_raw_data/config/project_manifest.yaml`](../00_raw_data/config/project_manifest.yaml) | project settings used for this step |

## Execution

This step was run from the `# Filter and normalize the data` and `# PRTC review and primary normalization` sections of [`proteomics_analysis.ipynb`](../scripts/notebooks/proteomics_analysis.ipynb), using the shared functions in [`filter_and_Normalize.py`](../scripts/python/filter_and_Normalize.py).

### QC and Normalization Summary

QC and normalization applied in this project:

| Done | Item | Value |
|------|------|-------|
| `⬜` | PRTC/internal standard rows reviewed | `{{ qc_prtc_reviewed }}` |
| `⬜` | PSM threshold applied before this step | `> {{ psm_threshold }}` |
| `⬜` | Zero-only rows removed | `{{ qc_zero_only_rows_removed }}` |
| `⬜` | Rows with excessive missingness removed | `{{ qc_missingness_rows_removed }}` |
| `⬜` | Missing values imputed | `{{ qc_missing_values_imputed }}` |
| `⬜` | Primary normalization method | `{{ primary_normalization }}` |
| `⬜` | Secondary normalization or correction | `{{ secondary_normalization }}` |
| `⬜` | Number of excluded samples | `{{ qc_excluded_sample_count }}` |
| `⬜` | Samples excluded after QC | `{{ qc_excluded_samples }}` |

Final sample set carried into [02_statistics](../02_statistics/README.md): `{{ final_sample_set }}`

## Output Files

| Name | Description |
|------|-------------|
| [`raw_abundance_matrix.csv`](./raw_abundance_matrix.csv) | extracted raw abundance matrix used before normalization |
| [`normalized_abundance_matrix.csv`](./normalized_abundance_matrix.csv) | primary normalized abundance matrix used for downstream comparisons |
| [`annotation.csv`](./annotation.csv) | feature annotation table carried forward into statistics |
| [`sample_metadata_used.csv`](./sample_metadata_used.csv) | validated sample metadata used during the notebook run |
| [`normalization_summary.csv`](./normalization_summary.csv) | normalization method summary |
| [`software_versions.txt`](./software_versions.txt) | runtime software versions captured during execution |

## Status & Notes

STATUS: `{{ qc_status }}`

- `{{ main_qc_note }}`
- `{{ normalization_note }}`
- `{{ carry_forward_note_for_statistics }}`
