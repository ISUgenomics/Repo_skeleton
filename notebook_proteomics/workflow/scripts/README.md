<!--
Editor notes:
- This file is an index of actual scripts present in scripts/.
- Update it when concrete scripts are added, removed, or changed in your proteomics pipeline.
-->
# scripts

Scripts used in the proteomics workflow.

The current shared codebase includes reusable Python and R scripts, executed directly or via jupyter notebook.

## Execution Order

- [01_qc_normalization](../01_qc_normalization/README.md): `python/filter_and_Normalize.py`
- [02_statistics](../02_statistics/README.md): `python/Stats.py`
- [03_visualization](../03_visualization/README.md): `python/volcano_plotter.py`, `python/heatmap_plotter.py`, `python/pca_plotter.py`
- [04_secondary_analyses](../04_secondary_analyses/README.md): `notebooks/Remake_Plots.ipynb`, and optionally `r/run_GO.R`

`notebooks/proteomics_analysis.ipynb` covers steps [01_qc_normalization](../01_qc_normalization/README.md), [02_statistics](../02_statistics/README.md), and [03_visualization](../03_visualization/README.md). It also creates `sample_metadata.csv` and `comparisons.csv` in [00_raw_data/config](../00_raw_data/config/README.md) if they are missing.

`python/config_gen.py` is the setup helper for creating `project_manifest.yaml` before the metadata and notebook stages. It also estimates `analysis.astral_mode` from the raw-data workbook when possible.

`python/metadata_gen.py` is the main setup helper for building `sample_metadata.csv` and, by default, `comparisons.csv` from either a metadata workbook/table or the raw-data file itself. When an external metadata file is present, it can infer the common header row and column mappings automatically if explicit selectors were not supplied.

`python/infer_astral_mode.py` is an optional inspection helper when you want a written rationale for the generated `astral_mode` value.

Documentation helper scripts are available in [python/docs](./python/docs/README.md).

Recommended startup path:

- place raw data and any metadata source file in `workflow/00_raw_data/`
- run `config_gen.py` to create `project_manifest.yaml`
- review and correct `project_manifest.yaml`
- run `metadata_gen.py --manifest ...`
- review or correct `sample_metadata.csv` and `comparisons.csv`
- run the notebook

## Script Index

### Python

| Script | Purpose | Inputs | Outputs | Notes |
|--------|---------|--------|---------|-------|
| [`filter_and_Normalize.py`](./python/filter_and_Normalize.py) | filtering, abundance extraction, normalization, and PRTC helper routines | raw data matrix, abundance columns | filtered and normalized matrices | current shared preprocessing and normalization module |
| [`Stats.py`](./python/Stats.py) | statistical testing, fold change calculation, and normality checks | normalized abundance matrix, sample groups | per-comparison statistics tables | taken from the cleaned `ProteomicsPipeline` core |
| [`volcano_plotter.py`](./python/volcano_plotter.py) | volcano plot generation | per-comparison statistics tables | HTML, PNG, SVG volcano plots | static exports label significant proteins |
| [`heatmap_plotter.py`](./python/heatmap_plotter.py) | heatmap generation | per-comparison statistics tables, sample groups | HTML, PNG, SVG heatmaps | use `--group1=value` and `--group2=value` when group labels begin with `-` |
| [`pca_plotter.py`](./python/pca_plotter.py) | PCA, 3D PCA, and PLS-DA plotting | normalized abundance matrix, sample groups | HTML, PNG, and SVG PCA/PLS-DA outputs | static PCA and PLS-DA exports label selected informative samples |
| [`helpers.py`](./python/helpers.py) | shared annotation, column rename, metadata-group lookup, and comparison-file helpers | input tables, metadata tables | helper functions for notebooks and scripts | supports both legacy metadata columns and template `sample_metadata.csv` columns |
| [`config_gen.py`](./python/config_gen.py) | generate `project_manifest.yaml` from the copied project structure | project root, raw data folder | `project_manifest.yaml` | detects the main raw data file, metadata source candidates, and estimates `analysis.astral_mode` from the workbook when possible |
| [`metadata_gen.py`](./python/metadata_gen.py) | generate `sample_metadata.csv` and, by default, `comparisons.csv` from a metadata file or raw-data starter path | metadata workbook or delimited file, or `project_manifest.yaml` with raw data | `sample_metadata.csv`, `comparisons.csv` | supports explicit `--header`, `--sample`, `--treatment`, repeatable `--factor name=column`, and optional `--group`, or can infer the common mapping automatically from an external metadata source |
| [`infer_astral_mode.py`](./python/infer_astral_mode.py) | inspect visible protein rows in a workbook and propose `analysis.astral_mode` | `project_manifest.yaml` or raw `.xlsx` workbook | console recommendation with zero-pattern summary | intended as a decision helper for zeros-as-missing versus legacy zero filtering |

### R

| Script | Purpose | Inputs | Outputs | Notes |
|--------|---------|--------|---------|-------|
| [`run_GO.R`](./r/run_GO.R) | GO and KEGG enrichment from comparison CSV outputs | comparison CSV directory with Entrez IDs | enrichment CSVs and dotplots | requires organism-specific review before use |

### Jupyter Notebook

| Script | Purpose | Inputs | Outputs | Notes |
|--------|---------|--------|---------|-------|
| [`proteomics_analysis.ipynb`](./notebooks/proteomics_analysis.ipynb) | main config-driven proteomics execution notebook | `project_manifest.yaml`, raw data file, optional `sample_metadata.csv`, optional `comparisons.csv` | QC outputs, comparison tables, visualization `output/HTML`, `output/PNG`, `output/SVG` folders, and missing startup config files when needed | standardized replacement for project-specific analysis notebooks |
| [`Remake_Plots.ipynb`](./notebooks/Remake_Plots.ipynb) | remake volcano and heatmap outputs with alternate thresholds | comparison CSV files, sample metadata | remade plots and markdown-ready output text | reusable follow-up notebook |
