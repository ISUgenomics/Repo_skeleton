# 04_Results

This file summarizes the workflow outputs, comparison-level findings, embedded figures, and manuscript-ready results text for the completed run.

- [**Significant Proteins**](#significant-proteins)
- [**Figure Browser**](#figure-browser)
- Per-step Summary
  - [1. QC and Normalization](#qc-and-normalization-summary)
  - [2. Statistics](#statistical-summary)
  - [3. Visualization](#visualization-summary)
- [**Manuscript-Style Summary**](#manuscript-style-summary)


## Significant Proteins

`{{ qvalue_summary }}` *See more in the [Statistical Summary](#statistical-summary) section.*

> cutoffs: **p**-value < 0.05 ; **q**-value < 0.05 ; abs(log2FC) > 1

{{ significant_proteins_table_md }}

---

{{ significant_hits_details_md }}

---

> **NOTE:** *This table is provided as an initial screening aid. For complete results interpretation, review all significant proteins, as other hits may prove interesting in your study.*

| Protein | Potential relevance to the hypothesis | Suggested literature evidence |
|---|---|---|
| `{{ hypothesis_hit_1_protein }}` | {{ hypothesis_hit_1_relevance }} | {{ hypothesis_hit_1_evidence }} |
| `{{ hypothesis_hit_2_protein }}` | {{ hypothesis_hit_2_relevance }} | {{ hypothesis_hit_2_evidence }} |


## Figure Browser

Each section below groups the main figure set for each requested contrast. *See more in the [Visualization Summary](#visualization-summary) section.*  
> **NOTE:** *`q-value`-based volcano plots remain available in the [output](./workflow/03_visualization/output/PNG/) folders but are not embedded here.*

<details><summary>Quick Plot Guide</summary>

| plot type | description | labeled entities |
|---|---|---|
| Volcano Plot | *The volcano plots summarize the significance of the proteins on the y-axis and the log2 fold change on the x-axis for each comparison. They are useful for showing how many proteins pass the selected thresholds and whether the strongest signal is balanced between positive and negative directions.* | significant proteins |
| Heatmap | *The heatmaps summarize the relative abundance patterns of the significant proteins across samples. Rows correspond to proteins, columns correspond to samples, and the color scale reflects log2-transformed abundance values. These plots are useful for showing whether samples cluster by condition and whether the same proteins drive separation across the comparison.* | - |
| PCA Plot | *The PCA plots summarize the largest sources of variation in the dataset by projecting samples onto the top principal components. These plots are useful for showing whether samples separate by biological group, whether replicates cluster together, and whether any sample appears to drive the overall variance disproportionately.* | samples that are both far from the plot origin and outlying within their group |
| 3D PCA Plot | *The 3D PCA plots extend the 2D PCA view by adding the third principal component, which can help clarify sample separation when the first two components alone do not fully resolve the groups. These interactive plots are useful for checking whether weak or ambiguous 2D patterns become more interpretable in three dimensions.* | - |
| PLS-DA Plot | *The PLS-DA plots summarize supervised separation between the compared groups. The ellipses indicate the approximate 95% confidence region for each group, and the cross-validation score helps assess how consistently each sample can be assigned to its expected class. These plots are useful for identifying comparisons with strong class separation as well as samples that behave ambiguously or may be difficult to classify robustly.* | low-confidence or misclassified samples identified during cross-validation |

</details>

<!-- Editor guide
Keep the figure-browser structure consistent across projects.

- Use one `<details>` block per enabled comparison.
- Add a nested `Samples` block.
- Keep the significant-protein tables in the dedicated `Significant Proteins` section above, not repeated here.
- Embed the main static figures below the tables in this order: volcano, heatmap, PCA panels, PLS-DA.
- If no q-value-significant proteins are present, keep q-value plots unembedded and explain that once above the comparison blocks.
-->

---

{{ figure_browser_sections_md }}

---

**Project-specific observations:**
{{ project_specific_visual_observations_md }}


## QC and Normalization Summary

| Item | Value |
|---|---|
| raw data file | [{{ raw_data_file }}](./workflow/00_raw_data/{{ raw_data_file }}) |
| analyzed samples | `{{ sample_count }}` |
| raw abundance matrix rows | `{{ raw_matrix_rows }}` |
| normalized abundance matrix rows | `{{ normalized_matrix_rows }}` |
| comparison tables | `{{ comparison_count }}` |

Supporting files:

- [workflow/01_qc_normalization/raw_abundance_matrix.csv](./workflow/01_qc_normalization/raw_abundance_matrix.csv)
- [workflow/01_qc_normalization/normalized_abundance_matrix.csv](./workflow/01_qc_normalization/normalized_abundance_matrix.csv)
- [workflow/01_qc_normalization/normalization_summary.csv](./workflow/01_qc_normalization/normalization_summary.csv)

<details><summary><b>Preview Insights</b></summary>

- **Were any samples excluded after QC?** `{{ qc_samples_excluded_summary }}`
- **Was the feature matrix reduced before statistics?** `{{ qc_matrix_change_summary }}`
- **What normalization path was used?** `{{ qc_normalization_summary }}`
- **Dataset-specific note:** `{{ qc_dataset_note }}`

</details>


## Statistical Summary

The completed workflow analyzed `{{ sample_count }}` samples and generated `{{ comparison_count }}` prespecified comparison tables from a normalized protein-abundance matrix containing `{{ normalized_matrix_rows }}` rows. At the reporting thresholds defined in [comparisons.csv](./workflow/00_raw_data/config/comparisons.csv), `{{ short_statistical_summary }}`.

> `p-value` - indicates proteins passing the nominal significance threshold before multiple-testing correction  <br>
> `q-value` - indicates proteins that remain significant after false-discovery-rate adjustment.

{{ significant_proteins_table_md }}

The summary file is [workflow/02_statistics/significant_protein_counts.csv](./workflow/02_statistics/significant_protein_counts.csv).

<details><summary><b>Preview Insights</b></summary>

- **Which comparison showed the strongest nominal signal?** `{{ strongest_nominal_comparison }}`
- **Which comparison showed the weakest nominal signal?** `{{ weakest_nominal_comparison }}`
- **Did any comparison retain FDR-supported proteins?** `{{ qvalue_summary }}`
- **Were nominally significant proteins observed on both fold-change sides?** `{{ fold_change_balance_summary }}`
- **Interesting dataset-specific pattern:** `{{ asymmetry_or_other_pattern }}`
- **What does this mean for the main biological questions?** `{{ conservative_biological_summary }}`

</details>


## Visualization Summary

Standard visualization outputs were generated for all requested comparisons.

| Plot type | Notes | Example |
|---|---|---|
| volcano plots | p-value and q-value volcano plots were generated for each comparison | [{{ example_volcano }}](./workflow/03_visualization/output/PNG/) |
| heatmaps | p-value heatmaps were generated for each comparison | [{{ example_heatmap }}](./workflow/03_visualization/output/PNG/) |
| PCA plots | `PC1 vs PC2`, `PC1 vs PC3`, and `PC2 vs PC3` panels were generated for each comparison, together with one 3D PCA plot | [{{ example_pca }}](./workflow/03_visualization/output/PNG/) |
| PLS-DA plots | one cross-validated PLS-DA plot was generated for each comparison | [{{ example_plsda }}](./workflow/03_visualization/output/PNG/) |

Plot files are under [workflow/03_visualization/output](./workflow/03_visualization/output), with format-specific subfolders [PNG](./workflow/03_visualization/output/PNG), [SVG](./workflow/03_visualization/output/SVG), and [HTML](./workflow/03_visualization/output/HTML).

<details><summary><b>Preview Insights</b></summary>

- **Which plot families were available for every contrast?** `{{ plot_family_summary }}`
- **Which result layer was most informative in this run?** `{{ p_or_q_layer_summary }}`
- **Which comparison had the clearest visual support overall?** `{{ visual_strongest }}`
- **Which comparison showed the weakest visual support?** `{{ visual_weakest }}`
- **What limited the visual value of the q-value-based figures?** `{{ qvalue_plot_limitations }}`

</details>


## Manuscript-Style Summary

Across the selected contrasts, differential abundance analysis identified proteins meeting the nominal p-value and fold-change criteria in `{{ result_summary_scope }}`. The largest nominal response was observed for `{{ strongest_comparison }}`, whereas `{{ weakest_comparison }}` produced the smallest nominal set. `{{ additional_result_counts_summary }}` No proteins remained significant after Benjamini-Hochberg false-discovery-rate correction at the selected thresholds `{{ qvalue_result_clause }}`.

The per-comparison figures further showed that `{{ main_visual_pattern }}`. Together, these results indicate `{{ concise_results_conclusion }}`.

## Next Step

Interpretation and biological context are provided in [06_Discussion.md](./06_Discussion.md).
