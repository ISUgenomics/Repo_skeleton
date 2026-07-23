# Workflow Implementation

This file explains the backend implementation.

<details><summary><b>Glossary</b></summary>

| Term | Meaning in this workflow |
|---|---|
| proteomics analysis | comparing protein-abundance measurements between biological sample groups |
| Excel spreadsheet | the starting input table for this workflow, with protein rows and sample-abundance columns |
| protein feature | one reported protein row in the spreadsheet, usually identified by accession and description |
| grouped abundance | the protein-level intensity value reported for one sample column |
| PSM | peptide-spectrum match count; used here as a support filter to remove weakly supported protein rows |
| PRTC | internal protein standard rows used for the main normalization step |
| normalization | rescaling abundance values so samples are more comparable before testing |
| comparison | one pairwise group test defined in `comparisons.csv` |
| fold change | the ratio of average abundance between the two compared groups |
| log2 fold change | fold change on a log2 scale, used to show both direction and effect size |
| p-value | nominal significance value before multiple-testing correction |
| q-value | false-discovery-rate adjusted p-value after Benjamini-Hochberg correction |
| astral mode | the workflow setting that makes zero handling more permissive during t-test filtering |
| Shapiro-Wilk test | a normality check run separately for each group in a comparison |
| volcano plot | plot combining significance and fold change for one comparison |
| heatmap | plot showing abundance patterns of selected proteins across samples |
| PCA | principal component analysis; an unsupervised summary of sample-level variation |
| PLS-DA | a supervised sample-separation method used here as a visualization aid |

</details>

## What This Workflow Does

In this workflow, proteomics analysis means comparing protein-abundance measurements between biologically defined sample groups. The input is an Excel spreadsheet in which rows represent protein features and columns include both annotation fields and grouped abundance signals for individual samples.

> The abundance signal used here is a protein-level grouped intensity table, typically exported from Thermo Scientific Proteome Discoverer. The workflow does not start from raw spectra; it starts from the processed abundance matrix after peptide identification and protein grouping have already been performed by the provider software.

The workflow then:
1. filters low-support proteins
2. extracts the abundance matrix
3. normalizes the sample columns
4. runs pairwise statistical comparisons
5. calculates fold changes and multiple-testing-adjusted q-values
6. writes per-comparison result tables and summary counts
7. generates review plots such as volcano plots, heatmaps, PCA, 3D PCA, and PLS-DA

## Implemented Methods

### 1. Row filtering

Purpose: this step removes proteins that are too weakly supported to interpret reliably and keeps the matrix focused on testable rows.

Implemented in [`scripts/python/filter_and_Normalize.py`](./scripts/python/filter_and_Normalize.py).

- The workflow locates the PSM column using `analysis.psm_column_contains`.
- PSM values are coerced to numeric before thresholding.
- Protein rows are retained when:
  - `PSM > psm_threshold` (*default:* `3`), or
  - the feature index starts with `PRTC-`
- After abundance extraction, proteins with total abundance `0` across all retained sample columns are removed.

Important detail:
- PRTC rows are preserved through early filtering because they are used for primary normalization.
- PRTC rows are removed before comparison statistics are written.

### 2. Primary normalization

Purpose: this step rescales the sample columns so they are more comparable before any group-level statistics are run.

Implemented by `normalize_prtc(...)` in [`scripts/python/filter_and_Normalize.py`](./scripts/python/filter_and_Normalize.py).

When `analysis.normalization_primary` is set to `PRTC` (*default:* `PRTC`), the implementation:
1. Collect rows whose identifiers start with `PRTC-`.
2. Replace `0` values in those rows with `NaN` so they do not contribute to the column median.
3. Compute one PRTC median per sample column.
4. Divide each sample column by its own PRTC median.
5. Multiply the rescaled columns by the mean of the PRTC medians to restore the matrix to a common scale.

Alternative primary normalization modes are controlled by `analysis.normalization_primary` (*default:* `PRTC`).

### 3. Comparison-level normalization

Purpose: this step optionally rescales each two-group subset again before testing, so the comparison is evaluated on a comparison-specific normalized matrix.

Implemented in [`scripts/python/Stats.py`](./scripts/python/Stats.py) via `uq_normalization(...)` from [`filter_and_Normalize.py`](./scripts/python/filter_and_Normalize.py).

When `analysis.apply_uq_per_comparison: true` (*default:* `true`):
- after subsetting the normalized matrix to the two groups for one comparison, an upper-quartile normalization step is applied again inside that comparison before statistics are calculated

This is an important backend assumption of the current workflow:
- the same globally normalized matrix is not always tested directly
- each comparison can be renormalized internally before its t-test is run

### 4. Statistical testing

Purpose: this step estimates whether the observed abundance differences between two groups are large enough, relative to within-group variation, to be treated as statistically notable.

Implemented in [`scripts/python/Stats.py`](./scripts/python/Stats.py).

For each enabled comparison row in [`comparisons.csv`](./00_raw_data/config/comparisons.csv), the workflow:
1. resolves sample columns from `sample_metadata.csv`
2. subsets the normalized matrix to those columns
3. optionally applies upper-quartile normalization within that subset
4. runs:
   - Student’s t-test
   - Shapiro-Wilk normality checks per group
   - fold-change calculation
5. joins those outputs with the annotation table using an inner join on feature ID

If a comparison row does not define its own grouping column, the fallback grouping column is `group` by default. Benjamini-Hochberg FDR is always used for q-value calculation.

#### Student’s t-test

Purpose: this is the core differential-abundance test used in the current workflow.

`perform_student_t_test(...)` uses:
- `scipy.stats.ttest_ind`
- `statsmodels.stats.multitest.multipletests(..., method='fdr_bh')`

Outputs written per feature:
- `studentT-testStatistic`
- `p-value_StudentTtest`
- `q-value_StudentTtest`
- `-log10(p-value_StudentTtest)`

#### Fold change

Purpose: this step gives the effect direction and size, not just significance.

`calculate_foldchange(...)` computes:
- `mean_expr_group1`
- `mean_expr_group2`
- `FoldChange = mean_group2 / mean_group1`
- `log2FoldChange = log2(FoldChange)`

Zeros are replaced with `NaN` before group means are calculated, so the group means are based on nonzero values.

#### Shapiro-Wilk

Purpose: this step records whether the nonzero values in each group look approximately normal under the Shapiro-Wilk test.

`test_shapiro_wilk_normality(...)` computes, for each group:
- `p-value_shapiro-G1`
- `p-value_shapiro-G2`
- `Normality-G1`
- `Normality-G2`

Only proteins with at least `3` nonzero values in each group enter the Shapiro-Wilk output.

### 5. Zero handling and `astral_mode`

Purpose: this setting controls how permissively the workflow treats zeros during pairwise testing.

When `analysis.astral_mode: true`:
- the workflow skips the stricter prefilter that would otherwise require:
  - at least `3` nonzero values in both groups, or
  - at least `3` nonzero values in one group with the other group entirely zero
- zeros are then handled more permissively inside the comparison logic

When `analysis.astral_mode: false` (*default in the statistics backend:* `false`):
- the workflow applies explicit comparison filters before testing
- zeros are trimmed more aggressively through the `retain_zeros(...)` logic

Important consequence:
- the t-test path can be permissive when `astral_mode` is enabled
- but the final exported comparison tables are still limited by the inner join with the Shapiro-Wilk output
- because Shapiro-Wilk only reports proteins with at least `3` nonzero values in each group, the final CSVs effectively retain that condition

So the final comparison tables reflect:
- permissive zero handling in the t-test calculation
- but a stricter reporting gate introduced by the merged Shapiro-Wilk output

### 6. Significance counting

Purpose: this step converts the full comparison tables into compact per-comparison hit counts for reporting.

Comparison-level hit counts are written to [02_statistics/significant_protein_counts.csv](./02_statistics/significant_protein_counts.csv).

Counts are based on the thresholds stored in each row of [`comparisons.csv`](./00_raw_data/config/comparisons.csv):
- `pvalue_cutoff`
- `qvalue_cutoff`
- `abs_log2fc_cutoff`

Common reporting defaults are `p < 0.05`, `q < 0.05`, and `abs(log2FC) > 1`.

The workflow counts:
- significant p-value hits: `p < cutoff` and `abs(log2FC) > cutoff`
- significant q-value hits: `q < cutoff` and `abs(log2FC) > cutoff`

## Visualization

### Volcano plots

Purpose: volcano plots summarize effect size and significance in one view, so they are the main scan plot for differential-abundance results.

Implemented in [`scripts/python/volcano_plotter.py`](./scripts/python/volcano_plotter.py).

- p-value volcano plots are always generated for enabled comparisons
- q-value volcano plots are also generated when `generate_qvalue_plots` is enabled (*default:* `true`)
- static `PNG` and `SVG` exports include labeled significant proteins

### Heatmaps

Purpose: heatmaps show whether the proteins passing the reporting thresholds form a coherent abundance pattern across the compared samples.

Implemented in [`scripts/python/heatmap_plotter.py`](./scripts/python/heatmap_plotter.py).

- heatmaps are generated from the proteins passing the selected p-value or q-value plus fold-change thresholds
- zeros are replaced with `NaN` before plotting
- heatmap values are shown on a log2 scale

### PCA and PLS-DA

Purpose: these plots summarize sample-level structure rather than protein-level significance, and help assess separation, clustering, and outliers.

Implemented in [`scripts/python/pca_plotter.py`](./scripts/python/pca_plotter.py).

- PCA plots are generated for `PC1 vs PC2`, `PC1 vs PC3`, and `PC2 vs PC3`
- one interactive 3D PCA plot is generated per comparison
- PLS-DA uses:
  - `StratifiedKFold`
  - `shuffle=True`
  - `random_state=42`
- the current plotting workflow uses up to `5` cross-validation splits, limited by the smallest group size

## Backend Assumptions

### Configurable

- raw input path and format
- identifier, PSM, and abundance column matching
- PSM threshold
- primary normalization mode
- whether per-comparison upper-quartile normalization is applied
- `astral_mode`
- comparison grouping, group labels, and thresholds
- q-value plot generation

### Fixed in the current implementation

- Student’s t-test is the differential-abundance engine
- Benjamini-Hochberg FDR is the multiple-testing method
- fold changes are computed from nonzero-only group means
- Shapiro-Wilk uses a minimum of `3` nonzero values per group
- final comparison CSVs are written from an inner join of t-test, Shapiro-Wilk, fold-change, and annotation outputs
- PLS-DA uses `StratifiedKFold` with `random_state=42`

### Practical consequences

- no separate missing-value imputation step is used
- zero handling is only partly explicit and is affected by `astral_mode`
- the final comparison tables can be stricter than the raw t-test path because Shapiro-Wilk output is joined in with `join='inner'`
- the workflow is pairwise by construction: each comparison row is analyzed independently
