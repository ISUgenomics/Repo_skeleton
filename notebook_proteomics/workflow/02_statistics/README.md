<!--
Editor notes:
- Document the actual comparisons run, the commands or notebook sections used, the result tables generated, and any deviations from the planned comparison set.
- The visible report should read like a completed run log, not a to-do list.
-->
# 02_statistics

Statistical analysis outputs.

*This step documents the differential abundance comparisons run for the project and the result tables generated from the normalized proteomics matrix. It records which comparisons were tested, which thresholds were applied, and where the main statistical signal was observed.*

## Input Files
<!-- List the files consumed by the statistics step. -->

Input files used for statistical testing:

| File | Purpose |
|------|---------|
| [`../00_raw_data/config/sample_metadata.csv`](../00_raw_data/config/sample_metadata.csv) | treatment groups and sample annotations |
| [`../00_raw_data/config/comparisons.csv`](../00_raw_data/config/comparisons.csv) | enabled comparisons and thresholds |
| `[fill in]` | normalized matrix from [01_qc_normalization](../01_qc_normalization/README.md) |

## Comparison Summary
<!-- List the actual comparisons executed and the output file generated for each. -->

Comparisons tested in this project:
- `[ ]` primary comparison set completed as defined in [`../00_raw_data/config/comparisons.csv`](../00_raw_data/config/comparisons.csv)
- `[ ]` one or more configured comparisons were skipped
- `[ ]` one or more additional comparisons were added during analysis

Statistical settings used in this step:

| Item | Value |
|------|-------|
| Statistical test or model | `[fill in]` |
| Grouping variable used for comparisons | `[fill in]` |
| Multiple-testing correction method | `[fill in]` |
| Significance thresholds | `p < [fill in]`, `q < [fill in]`, `|log2FC| >= [fill in]` |

| comparison_id | group1 | group2 | p-value cutoff | q-value cutoff | abs_log2fc cutoff | output file |
|---------------|--------|--------|----------------|----------------|-------------------|-------------|
| `[fill in]` | `[fill in]` | `[fill in]` | `0.05` | `0.05` | `1` | `[fill in]` |

## Number of significantly DE proteins
<!-- Report the main comparison counts from the generated statistical results. -->

| Comparison | Proteins with significant pvalue | Proteins with significant qvalue |
| -- | -- | -- |
| `[fill in]` | `[fill in]` | `[fill in]` |

## Execution
<!-- Record the direct script call(s) used for this step. In the visible narrative, name the notebook section that orchestrated the step for this project. -->

This step was run from the `# Run statistics and generate plots` section of [`proteomics_analysis.ipynb`](../scripts/notebooks/proteomics_analysis.ipynb).

```bash
python workflow/scripts/python/Stats.py run \
  --manifest workflow/00_raw_data/config/project_manifest.yaml
```

## Output Files
<!-- Record the files produced by the statistics step. -->

Statistical result files generated in this step:

| Name | Description |
|------|-------------|
| `[fill in or remove row]` | raw data table if saved |
| `[fill in or remove row]` | normalized data table if saved |
| `[fill in]` | per-comparison results table |
| `[fill in or remove row]` | summary table of significant proteins across comparisons |

## Results Summary
<!-- Record the main findings from this step using the actual statistics generated for the project. -->

The strongest differential abundance signal was observed in `[fill in comparison]`, with `[few / moderate / many]` proteins passing the nominal p-value threshold and `[few / moderate / many]` proteins retained after multiple-testing correction. Additional comparisons showed `[similar / weaker / no]` q-value-supported signal, and `[fill in comparison or remove phrase]` showed the weakest overall statistical separation.

<!-- (examples)
- Comparisons with the highest p-value-supported hit counts: `[fill in]`
- Comparisons retaining q-value-supported proteins: `[fill in or remove bullet]`
- Comparisons with no significant proteins after q-value filtering: `[fill in or remove bullet]`
-->

## Notes
<!-- Record issues, exceptions, or run-specific comments. -->

- Deviations from planned comparisons in [`../00_raw_data/config/comparisons.csv`](../00_raw_data/config/comparisons.csv): `[fill in or none]`
- Statistical method or threshold changes applied during the run: `[fill in or none]`
- Any caveat that should be carried into [03_visualization](../03_visualization/README.md) or [final_report](../final_report/README.md): `[fill in or remove bullet]`
