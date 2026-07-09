#### 03_Methods.md

<!--
Editor notes:
- Remove options not used in the project.
- Record exact versions, thresholds, and exceptions.
- If the project deviates from the default workflow, explain why.
-->

[Experimental Methods](#experimental-methods)
[Computational Methods](#computational-methods)
[Project-Specific Decisions](#project-specific-decisions)
[Manuscript Methods Paragraph](#manuscript-methods-paragraph)

---

- **Date created:** [YYYY-MM-DD]
- **Last updated:** [YYYY-MM-DD]

## Experimental Methods

| Step | Description |
|------|-------------|
| Organism / system | `[REQUIRED]` |
| Material / tissue | `[REQUIRED]` |
| Sample preparation | `[REQUIRED]` |
| Instrument / platform | `[REQUIRED]` |
| Search / identification software | `[REQUIRED]` |
| Export type | `[REQUIRED]` |

## Computational Methods

| check | step | tool / file | version | notes |
|-------|------|-------------|---------|-------|
| [x] | input inspection | provider export review | | |
| [x] | PSM filtering | `filter_and_normalize.py` or notebook cell | | |
| [x] | abundance cleanup | column extraction and rename rules | | |
| [x] | normalization | `PRTC`, `upper quartile`, or other | | |
| [x] | statistics | `scipy.stats.ttest_ind` or other | | |
| [x] | multiple testing | `statsmodels` FDR | | |
| [x] | visualization | volcano / heatmap / PCA / PLS-DA | | |
| [ ] | secondary comparison set | optional | | |
| [ ] | remake plots with altered thresholds | optional | | |

## Project-Specific Decisions

Document anything that is easy to leave hardcoded:

- rename rules used for provider columns
- treatment mapping dictionary
- group merge rules
- handling of zeros
- handling of technical replicates
- handling of extra samples
- Astral-specific or provider-specific branching

## Manuscript Methods Paragraph

Proteomic abundance data were obtained from `[REQUIRED: provider / platform]` and exported as `[REQUIRED: file type]`. The analysis used a project-specific visible-only or cleaned export defined in `01_Files.md`. Proteins were filtered to retain entries with peptide-spectrum match counts above `[REQUIRED threshold]`, while quality-control entries such as `PRTC` were handled according to the normalization workflow. Features with zero abundance across all included samples were removed prior to downstream analysis.

Sample-level abundances were normalized using `[REQUIRED: PRTC / upper quartile / other]`. For pairwise comparisons, the exact sample groupings and thresholds were defined in `comparisons.csv` and not hardcoded in the notebook. Differential abundance testing was performed using `[REQUIRED: Student's t-test / other]`, and p-values were adjusted using the Benjamini-Hochberg method. Results were summarized with volcano plots, heatmaps, principal component analysis, and partial least squares discriminant analysis where appropriate.
