<!--
Editor notes:
- Use this file as the technical output index for figures generated in this step.
- Keep the visible text factual and execution-focused.
- Keep biological interpretation of the figures in ../../04_Results.md.
-->
# 03_visualization

Visualization outputs from the proteomics analysis.

*This step documents the figures generated to review differential abundance results and sample-level structure in the dataset. It records which plot types were produced, which comparisons were visualized, and what technical checks were confirmed for the generated files.*  
*Interpretation of the generated figures is summarized in [04_Results.md](../../04_Results.md).*

- Files ending in `_P` use nominal p-value significance thresholds from the statistical analysis.
- Files ending in `_Q` use multiple-testing-adjusted q-value thresholds, where q-values are false-discovery-rate adjusted p-values.

Types of generated visual results in [workflow/03_visualization/output/](./output/):

| Name | Description |
| -- | -- |
| [CSV](./output/CSV/) | visualization-specific tables saved during plotting, if any |
| [HTML](./output/HTML/) | interactive plots, including volcano plots, heatmaps, PCA plots, 3D PCA plots, and PLS-DA plots |
| [PNG](./output/PNG/) | static plot exports for review and reporting |
| [SVG](./output/SVG/) | vector plot exports for manuscript or presentation use |

### Generated Comparisons

These visual results were generated for the following comparisons:
- `{{ comparison_1_label }}`
- `{{ comparison_2_label }}`
- `{{ comparison_3_label }}`
- `{{ comparison_4_label }}`

## Execution

- Notebook used to generate the figures: [`workflow/scripts/notebooks/proteomics_analysis.ipynb`](../scripts/notebooks/proteomics_analysis.ipynb)  
- Sample grouping file used by plotting steps: [`workflow/00_raw_data/config/sample_metadata.csv`](../00_raw_data/config/sample_metadata.csv)  
- Comparison definition file used by plotting steps: [`workflow/00_raw_data/config/comparisons.csv`](../00_raw_data/config/comparisons.csv)

**Plotting thresholds** used in this step: `p < 0.05`, `q < 0.05`, `abs(log2FC) > 1`

This step was run from the `# Run statistics and generate plots` section of [`proteomics_analysis.ipynb`](../scripts/notebooks/proteomics_analysis.ipynb), using the shared plotting functions in [`volcano_plotter.py`](../scripts/python/volcano_plotter.py), [`heatmap_plotter.py`](../scripts/python/heatmap_plotter.py), and [`pca_plotter.py`](../scripts/python/pca_plotter.py).

## Plot Summary

| Plot type | Generated | Notes |
|-----------|-----------|-------|
| [Volcano plots](#volcano-plots) | `{{ volcano_plots_generated }}` | p-value and q-value volcano plots were generated for enabled comparisons |
| [Heatmaps](#heatmaps) | `{{ heatmaps_generated }}` | p-value heatmaps were generated when significant proteins were available |
| [PCA plots](#pca-plots) | `{{ pca_plots_generated }}` | 2D PCA panels were generated in PNG, SVG, and HTML formats |
| [3D PCA plots](#3d-pca-plots) | `{{ pca_3d_plots_generated }}` | one interactive 3D PCA plot was generated per comparison |
| [PLS-DA plots](#pls-da-plots) | `{{ plsda_plots_generated }}` | cross-validated PLS-DA plots were generated in PNG, SVG, and HTML formats |

<!-- Editor guide:
- actively perform the checks below and convert them to `✅` only when verified
- keep only checks that apply to the project
- if an expected output is missing, say whether the cause was no plottable data, insufficient significant proteins, or a plotting/export failure
-->

### Volcano Plots

⬜ Files present for all enabled comparisons: `{{ volcano_files_present_list }}`
⬜ Expected formats present: `PNG`, `SVG`, and `HTML`
⬜ Both nominal and adjusted variants present for every comparison: `_P` and `_Q`
⬜ Static exports include significant-protein labels on `PNG` and `SVG`
⬜ q-value volcano plots were generated successfully or documented as not informative

### Heatmaps

⬜ Files present for all enabled comparisons: `{{ heatmap_files_present_list }}`
⬜ Expected formats present: `PNG`, `SVG`, and `HTML`
⬜ p-value heatmaps were generated for all expected comparisons
⬜ q-value heatmaps were either generated or correctly absent because no q-value-significant proteins were present

### PCA Plots

⬜ Files present for all enabled comparisons: `{{ pca_files_present_list }}`
⬜ Expected formats present: `PNG`, `SVG`, and `HTML`
⬜ All three 2D PCA pairings are present for every comparison: `PC1 vs PC2`, `PC1 vs PC3`, `PC2 vs PC3`
⬜ Static exports label selected informative samples on `PNG` and `SVG`

### 3D PCA Plots

⬜ Files present for all enabled comparisons: `{{ pca3d_files_present_list }}`
⬜ Expected format present: `HTML`
⬜ One 3D PCA plot was generated for each enabled comparison

### PLS-DA Plots

⬜ Files present for all enabled comparisons: `{{ plsda_files_present_list }}`
⬜ Expected formats present: `PNG`, `SVG`, and `HTML`
⬜ Static exports label samples with `CV_Score <= 0.6` or a cross-validation class mismatch
⬜ Cross-validation settings were verified for the current plotting workflow

## Status & Notes

STATUS: `{{ visualization_status }}`

- `{{ plot_generation_status_note }}`
