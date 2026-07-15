# 03_Methods

This file records the experimental context, computational workflow steps and project-specific settings, and manuscript-ready methods summary for the analysis.

- [Experimental Context](#experimental-context)
- [Computational Workflow](#computational-workflow)
  - [Analysis Steps](#analysis-steps)
- [Software Versions](#software-versions)
- [Manuscript-Style Summary](#manuscript-style-summary)

## Experimental Context

Proteomic abundance data were obtained from `{{ tissue_or_material }}` collected from `{{ organism_or_system }}` and analyzed by `{{ platform }}`. The raw data file used for the workflow was [{{ raw_data_file }}](./workflow/00_raw_data/), which should contain the expected grouped abundance columns and protein metadata fields.

## Computational Workflow

Protein abundance data were analyzed from the grouped-abundance raw-data file using the [notebook-based proteomics workflow](./workflow/scripts/notebooks/proteomics_analysis.ipynb) configured by [project_manifest.yaml](./workflow/00_raw_data/config/project_manifest.yaml), [sample_metadata.csv](./workflow/00_raw_data/config/sample_metadata.csv), and [comparisons.csv](./workflow/00_raw_data/config/comparisons.csv).

### Analysis Steps

1. Inspect the raw-data workbook or table and confirm that it is the correct starting input.
2. Filter proteins using the configured PSM threshold while retaining PRTC rows for normalization when applicable.
3. Extract and rename abundance columns to sample-level columns that match the metadata.
4. Normalize sample abundances using the configured primary normalization method.
5. Apply any configured comparison-level normalization before statistics.
6. Run Student's t-test, Shapiro-Wilk normality testing, fold-change calculation, and Benjamini-Hochberg FDR correction for each enabled comparison.
7. Generate CSV outputs, volcano plots, heatmaps, PCA plots, and PLS-DA plots.

**Project-specific notes**

- Proteins were retained for downstream analysis when peptide-spectrum match counts exceeded `{{ psm_threshold }}`, while PRTC rows were retained for normalization when applicable.
- Abundance columns matching `{{ abundance_column_pattern }}` were extracted from the raw data, renamed to sample-level columns, and aligned to the validated metadata table.
- The workflow was configured with `astral_mode: {{ astral_mode }}`, so zero values were treated as `{{ zero_handling_description }}`.
- Primary normalization was performed using `{{ primary_normalization }}`, followed by `{{ secondary_normalization }}`.
- Only the requested contrasts listed in [comparisons.csv](./workflow/00_raw_data/config/comparisons.csv) were enabled.

**Main settings used in the run**

| Setting | Value |
|---|---|
| input format | `{{ input_format }}` |
| PSM threshold | `> {{ psm_threshold }}` |
| abundance columns | `{{ abundance_column_pattern }}` |
| primary normalization | `{{ primary_normalization }}` |
| per-comparison upper quartile normalization | `{{ upper_quartile_normalization }}` |
| `astral_mode` | `{{ astral_mode }}` |
| q-value plots | `{{ qvalue_plots }}` |

| p-value cutoff | q-value cutoff | abs(log2FC) cutoff |
|---|---|---|
| `0.05` | `0.05` | `1` |

### Software Versions

The executed environment is recorded in [workflow/01_qc_normalization/software_versions.txt](./workflow/01_qc_normalization/software_versions.txt).

| Package | Version |
|---|---|
| Python | `{{ python_version }}` |
| numpy | `{{ numpy_version }}` |
| pandas | `{{ pandas_version }}` |
| scipy | `{{ scipy_version }}` |
| statsmodels | `{{ statsmodels_version }}` |
| plotly | `{{ plotly_version }}` |
| matplotlib | `{{ matplotlib_version }}` |
| seaborn | `{{ seaborn_version }}` |
| sklearn | `{{ sklearn_version }}` |

## Manuscript-Style Summary

Proteomic abundance data were analyzed from a grouped-abundance LC-MS/MS raw-data matrix using a notebook-based workflow parameterized by sample-metadata and comparison-definition files. Proteins were filtered using a peptide-spectrum match threshold greater than `{{ psm_threshold }}`, with PRTC entries retained for normalization when applicable. Sample-abundance columns were extracted from the raw data, harmonized to the curated metadata table, and normalized using `{{ primary_normalization }}` primary normalization followed by `{{ secondary_normalization }}`. The workflow was executed with `astral_mode: {{ astral_mode }}`, such that zero values were treated as `{{ zero_handling_description }}`.

Differential abundance analysis was performed separately for `{{ enabled_comparisons_summary }}`. For each contrast, Student's t-tests, Shapiro-Wilk normality tests, and fold-change calculations were applied to the normalized abundance matrix, and p-values were adjusted using the Benjamini-Hochberg false-discovery-rate procedure. Reporting thresholds were defined a priori as `p < 0.05`, `q < 0.05`, and `abs(log2FC) > 1`. Comparison-specific result tables were used to generate volcano plots, heatmaps, principal component analysis plots, and partial least squares discriminant analysis plots.
