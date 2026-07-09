<!--
Editor notes:
- Use this file as the output index and plot narrative for figures generated in this step.
- Keep the rendered text readable for a newcomer or collaborator who has not seen the notebook.
- For each plot family, list the files actually generated and add brief factual observations from visual review.
- Section comments should guide the executor on what to insert or look for, but should stay hidden in rendered output.
-->
# 03_visualization

Visualization outputs from the proteomics analysis.

*This step documents the figures generated to review differential abundance results and sample-level structure in the dataset. It records which plot types were produced, which comparisons were visualized, and what patterns were observed across the main plots.*

- Files ending in `_P` use nominal p-value significance thresholds from the statistical analysis.
- Files ending in `_Q` use multiple-testing-adjusted q-value thresholds, where q-values are false-discovery-rate adjusted p-values.

Types of generated visual results:

| Name | Description |
| -- | -- |
| CSV | Visualization-specific tables saved during plotting, if any |
| `output/HTML` | Interactive plots, including volcano plots, heatmaps, PCA plots, 3D PCA plots, and PLS-DA plots |
| `output/PNG` | Static plot exports for review and reporting |
| `output/SVG` | Vector plot exports for manuscript or presentation use |


### Generated Comparisons
<!-- List the comparisons for which plots were generated in this step. Use the comparison labels defined for this project in workflow/00_raw_data/config/comparisons.csv and keep the naming consistent with the generated files. Remove lines that do not apply. -->

These visual results were generated for the following comparisons:
- `[fill in comparison]`
- `[fill in comparison]`

<!-- (optional) 
Additional plots were reviewed for:
- `[fill in comparison or remove section]`
-->

## Execution

- Notebook used to generate the figures: [`workflow/scripts/notebooks/proteomics_analysis.ipynb`](../scripts/notebooks/proteomics_analysis.ipynb)  
- Sample grouping file used by plotting steps: `[fill in file name and path]`  
- Comparison definition file used by plotting steps: `workflow/00_raw_data/config/comparisons.csv`

**Plotting thresholds** used in this step: `p < [fill in]`, `q < [fill in]`, `|log2FC| >= [fill in]`

<!-- Record the command(s) or notebook execution used to generate the plots in this step. Keep only what applies for this project. -->

This step was run from the `# Run statistics and generate plots` section of [`proteomics_analysis.ipynb`](../scripts/notebooks/proteomics_analysis.ipynb).

```bash
python workflow/scripts/python/volcano_plotter.py \
  --input workflow/02_statistics/CSV/<group1>_vs_<group2>_comparison.csv \
  --output-dir workflow/03_visualization \
  --pvalue-limit 0.05 \
  --qvalue-limit 0.05 \
  --fold-change-limit 1

python workflow/scripts/python/heatmap_plotter.py \
  --input workflow/02_statistics/CSV/<group1>_vs_<group2>_comparison.csv \
  --metadata workflow/00_raw_data/config/sample_metadata.csv \
  --grouping-column group \
  --group1 <group1> \
  --group2 <group2> \
  --output-dir workflow/03_visualization \
  --pvalue-limit 0.05 \
  --qvalue-limit 0.05 \
  --fold-change-limit 1

python workflow/scripts/python/pca_plotter.py \
  --input workflow/01_qc_normalization/normalized_abundance_matrix.csv \
  --metadata workflow/00_raw_data/config/sample_metadata.csv \
  --grouping-column group \
  --group1 <group1> \
  --group2 <group2> \
  --output-dir workflow/03_visualization
```

<!-- (optional)
Plots were re-generated for `[fill in comparison / plot type / reason]`

```bash
python workflow/scripts/python/volcano_plotter.py \
  --input workflow/02_statistics/CSV/<group1>_vs_<group2>_comparison.csv \
  --output-dir workflow/04_secondary_analyses \
  --pvalue-limit 0.05 \
  --qvalue-limit 0.05 \
  --fold-change-limit 0
```

Plots were generated interactively in [`workflow/scripts/notebooks/proteomics_analysis.ipynb`](../scripts/notebooks/proteomics_analysis.ipynb):
```
[paste relevant code cell]
```
-->


## Plot Summary
<!-- Summarize the plot families actually generated for this project. -->

| Plot type | Generated | Notes |
|-----------|-----------|-------|
| [Volcano plots](#volcano-plots) | `[yes/no]` | |
| [Heatmaps](#heatmaps) | `[yes/no]` | |
| [PCA plots](#pca-plots) | `[yes/no]` | |
| [3D PCA plots](#3d-pca-plots) | `[yes/no]` | |
| [PLS-DA plots](#pls-da-plots) | `[yes/no]` | |

<!-- Record any overall observations from the visual review across plot types. -->

The visual review showed that `[fill in comparison or condition]` had the clearest overall separation across the generated plots, whereas `[fill in comparison or remove phrase]` showed weaker or less consistent signal. In general, the main patterns were `[consistent across plot types / partially consistent across plot types / driven mainly by one plot family]`, and `[q-value filtering preserved the strongest findings / q-value filtering substantially reduced the visible signal / remove phrase if not applicable]`.


### Volcano Plots
<!-- List the volcano plots generated in this step. Add one or two factual lines about what stood out:
- whether there were many significant features
- whether the signal was balanced or one-sided
- whether q-value filtering substantially reduced the hits
-->

*The volcano plots summarize the significance of the proteins on the y-axis and the log2 fold change on the x-axis for each comparison. They are useful for showing how many proteins pass the selected thresholds and whether the strongest signal is balanced between positive and negative directions.*

<!-- Suggested insertion pattern.
#### output/PNG/volcano_plot_<comparison_id>_P.png
![](output/PNG/volcano_plot_<comparison_id>_P.png)

The nominal p-value volcano plots showed that `[fill in comparison]` had `[few / moderate / many]` proteins passing the p-value threshold, whereas `[fill in comparison or remove phrase]` showed `[weaker / stronger / more asymmetric]` signal. 

#### output/PNG/volcano_plot_<comparison_id>_Q.png
![](output/PNG/volcano_plot_<comparison_id>_Q.png)

After multiple-testing correction, the q-value volcano plots showed that `[fill in comparison]` retained `[few / moderate / many]` significant proteins, while q-value filtering `[greatly reduced / moderately reduced / minimally changed]` the highlighted set in `[fill in comparison or remove phrase]`.
-->

**Key insights:**
<!-- (examples)
- Comparisons with the strongest volcano plot signal: `[fill in]`
- Comparisons with little or no q-value-supported signal: `[fill in or remove bullet]`
- Any one-sided shift or unusual distribution worth noting: `[fill in or remove bullet]`
-->


### Heatmaps
<!-- List the heatmaps generated in this step. Add one or two factual lines about whether samples clustered by group, whether separation was clear or mixed, and whether the q-value heatmap still retained enough proteins to be informative. -->

*The heatmaps summarize the relative abundance patterns of the significant proteins across samples. Rows correspond to proteins, columns correspond to samples, and the color scale reflects log2-transformed abundance values. These plots are useful for showing whether samples cluster by condition and whether the same proteins drive separation across the comparison.*

<!-- Suggested insertion pattern.
#### output/PNG/Heatmap_<comparison_id>_P.png
![](output/PNG/Heatmap_<comparison_id>_P.png)

The nominal p-value heatmaps showed that samples from `[fill in comparison]` `[clustered clearly by group / showed partial separation / showed mixed clustering]`, with `[a small / a moderate / a broad]` set of proteins contributing to the observed pattern.

#### output/PNG/Heatmap_<comparison_id>_Q.png
![](output/PNG/Heatmap_<comparison_id>_Q.png)

After multiple-testing correction, the q-value heatmaps showed that `[fill in comparison]` retained `[clear / limited / no]` group-specific structure, and q-value filtering `[preserved the main pattern / reduced the number of informative proteins / left too few proteins for a stable visual pattern]`.
-->

**Key insights:**
<!-- (examples)
- Comparisons with the clearest sample clustering by group: `[fill in]`
- Comparisons where clustering weakened after q-value filtering: `[fill in or remove bullet]`
- Any mixed samples, weak separation, or within-group heterogeneity worth noting: `[fill in or remove bullet]`
-->

### PCA Plots
<!-- List the 2D PCA plots generated in this step. Add one or two factual lines about whether separation was visible on the main principal components, whether any sample behaved as an outlier, and whether the dominant variance appeared to reflect biology or technical noise. -->

*The PCA plots summarize the largest sources of variation in the dataset by projecting samples onto the top principal components. These plots are useful for showing whether samples separate by biological group, whether replicates cluster together, and whether any sample appears to drive the overall variance disproportionately.*

<!-- Suggested insertion pattern.
#### output/PNG/PCA_<comparison_id>_PC1_vs_PC2.png
![](output/PNG/PCA_<comparison_id>_PC1_vs_PC2.png)

#### output/PNG/PCA_<comparison_id>_PC1_vs_PC3.png
![](output/PNG/PCA_<comparison_id>_PC1_vs_PC3.png)

#### output/PNG/PCA_<comparison_id>_PC2_vs_PC3.png
![](output/PNG/PCA_<comparison_id>_PC2_vs_PC3.png)

The PCA plots showed that samples from `[fill in comparison]` `[separated clearly / separated partially / overlapped substantially]` across the main principal components. Replicates were `[tightly clustered / moderately dispersed / highly variable]`, and `[no obvious outliers were observed / sample <sample_id> appeared offset from the remaining replicates]`.
-->

**Key insights:**
<!-- (examples)
- Comparisons with the clearest PCA-based group separation: `[fill in]`
- Any outlier or unusually dispersed samples: `[fill in or remove bullet]`
- Whether the main variance appeared to reflect biology, batch effects, or mixed structure: `[fill in or remove bullet]`
-->


### 3D PCA Plots
<!-- List the interactive 3D PCA plots generated in this step, if any. Add one or two factual lines about whether the third principal component improved separation, clarified overlap seen in 2D PCA, or revealed outliers not obvious in the static plots. -->

*The 3D PCA plots extend the 2D PCA view by adding the third principal component, which can help clarify sample separation when the first two components alone do not fully resolve the groups. These interactive plots are useful for checking whether weak or ambiguous 2D patterns become more interpretable in three dimensions.*

<!-- Suggested insertion pattern.
#### output/HTML/3D_PCA_<comparison_id>.html
[3D_PCA_<comparison_id>.html](output/HTML/3D_PCA_<comparison_id>.html)

The 3D PCA plots showed that including the third principal component `[improved separation between groups / did not materially change the interpretation / highlighted one or more samples with intermediate positioning]` for `[fill in comparison]`.
-->

**Key insights:**
<!-- (examples)
- Comparisons where 3D PCA improved interpretation relative to 2D PCA: `[fill in]`
- Any outliers or intermediate samples revealed more clearly in 3D: `[fill in or remove bullet]`
- Whether 3D PCA confirmed or weakened the pattern seen in the 2D PCA plots: `[fill in or remove bullet]`
-->


### PLS-DA Plots
<!-- List the PLS-DA or PLS-DA cross-validation plots generated in this step. Add one or two factual lines about whether the group ellipses were clearly separated, whether any samples fell near the opposite group, and whether the cross-validation scores suggested stable or borderline classification. -->

*The PLS-DA plots summarize supervised separation between the compared groups. The ellipses indicate the approximate 95% confidence region for each group, and the cross-validation score helps assess how consistently each sample can be assigned to its expected class. These plots are useful for identifying comparisons with strong class separation as well as samples that behave ambiguously or may be difficult to classify robustly.*

<!-- Suggested insertion pattern.
#### output/PNG/PLS-DA_CV_Ellipses_<comparison_id>.png
![](output/PNG/PLS-DA_CV_Ellipses_<comparison_id>.png)

The PLS-DA plots showed that `[fill in comparison]` had `[clear / partial / weak]` separation between groups, with `[little / some / substantial]` overlap between the confidence ellipses. Cross-validation suggested that classification was `[generally stable / mixed across samples / borderline for one or more samples]`, and `[sample <sample_id> / no individual sample]` stood out as potentially difficult to classify consistently.

This plot was interpreted as `[exploratory support for group separation / supportive but not decisive evidence / weak or unstable separation]` based on the observed cross-validation behavior.
-->

**Key insights:**
<!-- (examples)
- Comparisons with the strongest supervised separation: `[fill in]`
- Comparisons with ellipse overlap or borderline classification: `[fill in or remove bullet]`
- Any individual samples with weak or ambiguous cross-validation support: `[fill in or remove bullet]`
- Cross-validation approach used for PLS-DA in this project: `[fill in]`
-->
