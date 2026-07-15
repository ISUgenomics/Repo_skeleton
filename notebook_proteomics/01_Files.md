# 01_Files

This file inventories the main project inputs, configuration files, and output locations used in the workflow.

- [Raw Data](#raw-data)
- [Workflow Configuration](#workflow-configuration)
- [Output Layout](#output-layout)

## Raw Data

| File | Role | Notes |
|---|---|---|
| [{{ raw_data_file }}](./workflow/00_raw_data/) | main raw data file | `{{ raw_data_notes }}` |
| [{{ metadata_source_file }}](./workflow/00_raw_data/) | metadata source | `{{ metadata_source_notes }}` |

## Workflow Configuration

| File | Role | Notes |
|---|---|---|
| [workflow/00_raw_data/config/project_manifest.yaml](./workflow/00_raw_data/config/project_manifest.yaml) | project manifest | run settings, file paths, and workflow options |
| [workflow/00_raw_data/config/sample_metadata.csv](./workflow/00_raw_data/config/sample_metadata.csv) | sample metadata | finalized sample annotations used by the notebook |
| [workflow/00_raw_data/config/comparisons.csv](./workflow/00_raw_data/config/comparisons.csv) | comparison table | finalized enabled-comparison analysis plan |

**Notes**

- See [workflow/00_raw_data/README.md](./workflow/00_raw_data/README.md) for raw-data intake details.
- visible-only raw-data copy: `{{ visible_only_copy_status }}`

## Output Layout

- QC and normalization: [workflow/01_qc_normalization](./workflow/01_qc_normalization/)
- Statistics tables: [workflow/02_statistics](./workflow/02_statistics/)
- Figures and interactive plots: [workflow/03_visualization](./workflow/03_visualization/)
- Scripts and helpers: [workflow/scripts](./workflow/scripts/)

| Key Output | File or folder |
|---|---|
| raw abundance matrix | [workflow/01_qc_normalization/raw_abundance_matrix.csv](./workflow/01_qc_normalization/raw_abundance_matrix.csv) |
| normalized abundance matrix | [workflow/01_qc_normalization/normalized_abundance_matrix.csv](./workflow/01_qc_normalization/normalized_abundance_matrix.csv) |
| normalization summary | [workflow/01_qc_normalization/normalization_summary.csv](./workflow/01_qc_normalization/normalization_summary.csv) |
| annotation table | [workflow/01_qc_normalization/annotation.csv](./workflow/01_qc_normalization/annotation.csv) |
| software versions | [workflow/01_qc_normalization/software_versions.txt](./workflow/01_qc_normalization/software_versions.txt) |
| comparison tables | [workflow/02_statistics/CSV](./workflow/02_statistics/CSV) |
| significant-hit summary | [workflow/02_statistics/significant_protein_counts.csv](./workflow/02_statistics/significant_protein_counts.csv) |
| plots | [workflow/03_visualization/output](./workflow/03_visualization/output) |
| main notebook | [workflow/scripts/notebooks/proteomics_analysis.ipynb](./workflow/scripts/notebooks/proteomics_analysis.ipynb) |
