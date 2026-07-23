# 03_Methods

This file records the experimental context, computational workflow steps and project-specific settings, and manuscript-ready methods summary for the analysis.

- [Experimental Context](#experimental-context)
- [Computational Workflow](#computational-workflow)
  - [Analysis Steps](#analysis-steps)
- [Software Versions](#software-versions)
- [Manuscript-Style Summary](#manuscript-style-summary)

## Experimental Context

Proteomic abundance data were obtained from `{{ tissue_or_material }}` collected from `{{ organism_or_system }}` and analyzed by `{{ platform }}`. The raw data file used for the workflow was [{{ raw_data_file }}](./workflow/00_raw_data/{{ raw_data_file }}), which should contain the expected grouped abundance columns and protein metadata fields.

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

Raw proteomics data were obtained from Thermo Scientific Proteome Discoverer output tables and imported into Python for downstream processing. Proteins supported by fewer than `{{ psm_threshold }}` peptide-spectrum matches (PSMs) were removed, while PRTC entries were retained for normalization when applicable. Proteins with zero abundance across all samples were excluded. Primary normalization used `{{ primary_normalization }}`, and an additional `{{ secondary_normalization }}` step was applied within each defined group comparison before statistical testing. Under the `astral` setting used in this workflow, zero abundance values were retained in the comparison matrix, and no separate missing-value imputation step was applied.

Differential abundance analysis was performed separately for the defined pairwise group comparisons. Student's t-tests, Shapiro-Wilk normality tests, and fold-change calculations were applied to the normalized abundance matrix, and p values were adjusted for multiple testing using the Benjamini-Hochberg false-discovery-rate procedure. For each comparison, proteins were reported only when at least 3 nonzero abundance values were present in each group. Python `{{ python_version }}` was used for data import, preprocessing, and figure generation, with `numpy {{ numpy_version }}`, `pandas {{ pandas_version }}`, `scipy {{ scipy_version }}`, `statsmodels {{ statsmodels_version }}`, `plotly {{ plotly_version }}`, `matplotlib {{ matplotlib_version }}`, `seaborn {{ seaborn_version }}`, and `sklearn {{ sklearn_version }}`.
