#### 01_Files.md

<!--
Editor notes:
- This file should list actual project files, not examples from older projects.
- If a row is not used, delete it.
- If the provider file was edited before analysis, record both original and cleaned versions.
-->

[Raw and Source Files](#raw-and-source-files)
[Metadata Files](#metadata-files)
[Processed Outputs](#processed-outputs)
[Notebook and Script Outputs](#notebook-and-script-outputs)

---

- **Date created:** [YYYY-MM-DD]
- **Last updated:** [YYYY-MM-DD]
- **Primary analysis location:** `[REQUIRED]`

## Raw and Source Files

| File role | File name | Format | Source | Location | Notes |
|-----------|-----------|--------|--------|----------|-------|
| Provider export | `[REQUIRED]` | `.xlsx/.txt/.tsv` | `[REQUIRED]` | `[REQUIRED]` | main source used for analysis |
| Visible-only export | `[REQUIRED if used]` | `.xlsx/.csv/.tsv` | generated from provider export | `[REQUIRED]` | if hidden rows/cells were removed |
| Original metadata file | `[REQUIRED if separate]` | `.xlsx/.csv/.tsv` | `[REQUIRED]` | `[REQUIRED]` | source metadata |

## Metadata Files

| File | Purpose | Location |
|------|---------|----------|
| `sample_metadata.csv` | curated sample table used by scripts and notebook | `workflow/00_raw_data/config/` |
| `comparisons.csv` | requested comparisons and thresholds | `workflow/00_raw_data/config/` |
| `project_manifest.yaml` | project-level settings | `workflow/00_raw_data/config/` |

## Processed Outputs

| File type | Description | Format | Filename(s) | Location |
|-----------|-------------|--------|-------------|----------|
| filtered matrix | PSM-filtered or cleaned abundance data | `.csv` | `[REQUIRED]` | `workflow/00_raw_data/` |
| normalized matrix | post-normalization abundance data | `.csv` | `[REQUIRED]` | `workflow/01_qc_normalization/` |
| comparison results | per-comparison stats tables | `.csv` | `[REQUIRED]` | `workflow/02_statistics/` |
| plot files | volcano, heatmap, PCA, PLS-DA | `.png/.svg/.html` | `[REQUIRED]` | `workflow/03_visualization/` |

## Notebook and Script Outputs

| File type | Description | Location |
|-----------|-------------|----------|
| notebook | main analysis notebook | `[REQUIRED]` |
| markdown export | notebook rendered to markdown if generated | `[REQUIRED or remove]` |
| helper scripts | reusable plotting/stats scripts | `workflow/scripts/` |
