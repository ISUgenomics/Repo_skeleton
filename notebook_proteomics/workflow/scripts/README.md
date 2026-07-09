<!--
Editor notes:
- This file is an index of actual scripts present in scripts/.
- Update it when concrete scripts are added, removed, or changed in your proteomics pipeline.
-->
# scripts

Scripts used in the proteomics workflow.

The current shared codebase includes reusable Python and R scripts, executed directly or via jupyter notebook.


## Execution Order
<!-- Record the actual execution order only after scripts exist and are used in the workflow. Cross-link to the workflow steps where each script is used when applicable. -->

- [01_qc_normalization](../01_qc_normalization/README.md): `python/filter_and_Normalize.py`
- [02_statistics](../02_statistics/README.md): `python/Stats.py`
- [03_visualization](../03_visualization/README.md): `python/volcano_plotter.py`, `python/heatmap_plotter.py`, `python/pca_plotter.py`
- [04_secondary_analyses](../04_secondary_analyses/README.md): `notebooks/Remake_Plots.ipynb`, and optionally `r/run_GO.R`

`notebooks/proteomics_analysis.ipynb` covers steps [01_qc_normalization](../01_qc_normalization/README.md), [02_statistics](../02_statistics/README.md), and [03_visualization](../03_visualization/README.md).
`python/bootstrap_config.py` is an optional setup helper before [00_raw_data](../00_raw_data/README.md) is finalized.


## Script Index
<!-- Document only scripts that are actually present in this directory and keep the entries consistent with the workflow steps that use them. -->

### Python 

| Script | Purpose | Inputs | Outputs | Notes |
|--------|---------|--------|---------|-------|
| [`filter_and_Normalize.py`](./python/filter_and_Normalize.py) | Filtering, abundance extraction, normalization, and PRTC helper routines | provider export matrix, abundance columns | filtered and normalized matrices | Current shared preprocessing and normalization module |
| [`Stats.py`](./python/Stats.py) | Statistical testing, fold change calculation, and normality checks | normalized abundance matrix, sample groups | per-comparison statistics tables | Taken from the cleaned `ProteomicsPipeline` core |
| [`volcano_plotter.py`](./python/volcano_plotter.py) | Volcano plot generation | per-comparison statistics tables | HTML, PNG, SVG volcano plots | Used by main analysis notebooks and `Remake_Plots.ipynb` |
| [`heatmap_plotter.py`](./python/heatmap_plotter.py) | Heatmap generation | per-comparison statistics tables, sample groups | HTML, PNG, SVG heatmaps | Used by main analysis notebooks and `Remake_Plots.ipynb` |
| [`pca_plotter.py`](./python/pca_plotter.py) | PCA, 3D PCA, and PLS-DA plotting | normalized abundance matrix, sample groups | HTML and PNG PCA/PLS-DA outputs | Current shared plotting module |
| [`helpers.py`](./python/helpers.py) | Shared annotation, column rename, metadata-group lookup, and comparison-file helpers | input tables, metadata tables | helper functions for notebooks and scripts | Supports both legacy metadata columns and template `sample_metadata.csv` columns |
| [`bootstrap_config.py`](./python/bootstrap_config.py) | Bootstrap `project_manifest.yaml` and `sample_metadata.csv` from a provider export | provider export, optional legacy metadata file | starter config files | Best suited to the common visible-only Excel exports used in current example projects |

### R 

| Script | Purpose | Inputs | Outputs | Notes |
|--------|---------|--------|---------|-------|
| [`run_GO.R`](./r/run_GO.R) | GO and KEGG enrichment from comparison CSV outputs | comparison CSV directory with Entrez IDs | enrichment CSVs and dotplots | Current R enrichment script from `ProteomicsPipeline`; currently mouse-oriented and requires organism-specific review before use |


### Jupyter Notebook

| Script | Purpose | Inputs | Outputs | Notes |
|--------|---------|--------|---------|-------|
| [`proteomics_analysis.ipynb`](./notebooks/proteomics_analysis.ipynb) | Main config-driven proteomics execution notebook | `project_manifest.yaml`, `sample_metadata.csv`, `comparisons.csv`, provider export | QC outputs, comparison tables, and visualization `output/HTML`, `output/PNG`, `output/SVG` folders | Standardized replacement for project-specific `P####_analysis.ipynb` notebooks |
| [`Remake_Plots.ipynb`](./notebooks/Remake_Plots.ipynb) | Re-make volcano and heatmap outputs with alternate thresholds | comparison CSV files, sample metadata | remade plots and markdown-ready output text | Reusable follow-up notebook adapted from `ProteomicsPipeline/Notebook_Sharu` |

