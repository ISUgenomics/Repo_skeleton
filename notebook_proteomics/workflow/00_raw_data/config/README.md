<!--
Editor notes:
- Keep this file as a short index of the project input files stored in config/.
-->
# config

Project startup files stored in [workflow/00_raw_data/config/](./).

## Contents

- [`project_manifest.yaml`](./project_manifest.yaml)
- [`sample_metadata.csv`](./sample_metadata.csv)
- [`comparisons.csv`](./comparisons.csv)

## Purpose

- `project_manifest.yaml`: minimal starting settings used to open the raw data file and control the analysis
- `sample_metadata.csv`: sample annotations and grouping fields created by the notebook if missing, or created up front from an external metadata source file with `metadata_gen.py`, then reviewed and reused across the workflow
- `comparisons.csv`: comparison definitions used for [02_statistics](../../02_statistics/README.md) and [03_visualization](../../03_visualization/README.md); may be created by the notebook if missing

## Key columns

[sample_metadata.csv](./sample_metadata.csv)

| Column | Meaning |
|------|---------|
| `sample_id` | stable sample identifier used in project notes |
| `source_column` | exact column name expected after abundance-column renaming |
| `treatment` | primary treatment-level grouping used in comparisons when applicable |
| additional factor columns | optional second or later experimental dimensions created from repeated `--factor name=column` inputs |
| `group` | broader grouping used in comparisons when applicable |
| `replicate` | replicate number within the chosen grouping |
| `batch_or_run` | file, run, or batch label if useful |
| `include` | `TRUE` or `FALSE` to include the sample in analysis |
| `notes` | optional project-specific comment |

[comparisons.csv](./comparisons.csv)

| Column | Meaning |
|------|---------|
| `comparison_id` | stable label for the comparison |
| `grouping_column` | metadata column used to resolve the samples, for example `treatment` or `group` |
| `group1` | first comparison label from `sample_metadata.csv` |
| `group2` | second comparison label from `sample_metadata.csv` |
| `use_qvalue` | whether q-value outputs are expected for this comparison |
| `pvalue_cutoff` | p-value threshold used in plots and summaries |
| `qvalue_cutoff` | q-value threshold used in plots and summaries |
| `abs_log2fc_cutoff` | absolute log2 fold-change threshold |
| `enabled` | `TRUE` or `FALSE` to run the comparison |
| `notes` | optional comment for project-specific handling |

## Important startup settings

- `project_manifest.yaml -> inputs.raw_data_file`: main raw Excel or text file used to start the analysis
- `project_manifest.yaml -> inputs.metadata_source`: optional metadata workbook/table used by `metadata_gen.py` before notebook launch
- `project_manifest.yaml -> inputs.comparisons_mode`: set to `generated` to let the workflow create/update `comparisons.csv` from `sample_metadata.csv`, or `manual` to preserve a hand-edited comparisons file
- `project_manifest.yaml -> analysis.normalization_primary`: main normalization path. Common values are `PRTC`, `control_run_quartile`, or `none`
- `project_manifest.yaml -> analysis.astral_mode`: controls whether zeros in comparison subsets are treated as missing-value placeholders during the t-test filtering step
- `project_manifest.yaml -> analysis.post_normalization_column_merges`: optional technical-replicate merge rules applied after primary normalization and before statistics
