<!--
Editor notes:
- Keep this file as a short index of the project input files stored in config/.
-->
# config

Project input files stored in `config/`.

## Contents

- [`project_manifest.yaml`](./project_manifest.yaml)
- [`sample_metadata.csv`](./sample_metadata.csv)
- [`comparisons.csv`](./comparisons.csv)

## Purpose

- `project_manifest.yaml`: project-level paths, analysis settings, and output locations referenced across the workflow
- `sample_metadata.csv`: sample annotations and grouping fields used in [01_qc_normalization](../../01_qc_normalization/README.md), [02_statistics](../../02_statistics/README.md), and [03_visualization](../../03_visualization/README.md)
- `comparisons.csv`: comparison definitions and thresholds used for [02_statistics](../../02_statistics/README.md) and [03_visualization](../../03_visualization/README.md)

## Key columns

`sample_metadata.csv`

| Column | Meaning |
|------|---------|
| `sample_id` | stable sample identifier used in project notes |
| `source_column` | exact column name expected after abundance-column renaming |
| `treatment` | treatment-level grouping used in comparisons when applicable |
| `group` | broader grouping used in comparisons when applicable |
| `replicate` | replicate number within the chosen grouping |
| `batch_or_run` | file, run, or batch label if useful |
| `include` | `TRUE` or `FALSE` to include the sample in analysis |
| `notes` | optional project-specific comment |

`comparisons.csv`

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

## Important execution flag

- `project_manifest.yaml -> flags.astral_mode`: controls whether zeros in comparison subsets are treated as missing-value placeholders during the t-test filtering step. Keep this aligned with the original project workflow when reproducing an existing analysis.
