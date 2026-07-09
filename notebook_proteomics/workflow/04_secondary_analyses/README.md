<!--
Editor notes:
- Use this file only when the project includes additional comparisons, remade plots, alternative thresholds, or other follow-up analyses beyond the main run.
- Keep the visible text factual and specific to the follow-up work that was actually performed.
- Remove the 04_secondary_analyses folder, if not applicable in your project.
-->
# 04_secondary_analyses

Secondary analyses and follow-up outputs.

*This step documents any follow-up analyses performed after the main proteomics workflow. It captures additional comparisons, remade plots, threshold changes, or other requested outputs that extend or refine the main interpretation.*

## Follow-Up Summary
<!-- State what follow-up was requested or performed. -->

These results are from the follow-up analyses performed after the main workflow.

Requested follow-up:
- `[fill in or remove bullet]`

Reason for follow-up:
- `[fill in or remove bullet]`

## Comparison or Output Scope
<!-- List the follow-up comparisons or output scope covered here. -->

Follow-up scope for this project:
- `[ ]` second comparison set
- `[ ]` remade plots using different thresholds
- `[ ]` focused subgroup analysis
- `[ ]` selected figure remake for reporting
- `[ ]` additional client-requested output
- `[ ]` other: `[fill in or remove bullet]`

Follow-up analyses covered `[fill in comparisons, outputs, or question addressed]`.

Where applicable, these follow-up outputs should be interpreted together with the main results in [02_statistics](../02_statistics/README.md) and [03_visualization](../03_visualization/README.md).

<!-- (optional)
Additional scope included:
- `[fill in or remove bullet]`
-->

## Output Files
<!-- List the output folders and the notebook or script actually used for this follow-up. -->

Follow-up outputs generated in this step:

| Name | Description |
| -- | -- |
| CSV | Output CSV files for follow-up comparisons or remade result tables |
| HTML | Output plots in HTML format, if generated |
| PNG | Output plots in PNG format |
| SVG | Vector plots for manuscript or reporting use |
| `[fill in notebook or script name]` | Notebook or script used for the follow-up |

## Number of significantly DE proteins
<!-- Report the main comparison counts from the follow-up statistical results, if applicable. Remove this section if the follow-up did not produce comparison-level hit counts. -->

| Comparison | Proteins with significant pvalue | Proteins with significant qvalue |
| -- | -- | -- |
| `[fill in]` | `[fill in]` | `[fill in]` |

## Execution
<!-- Record the direct script call(s) or notebook used for this step. In the visible narrative, name the notebook section or follow-up notebook that orchestrated the step for this project. -->

This step was run from the follow-up notebook [`Remake_Plots.ipynb`](../scripts/notebooks/Remake_Plots.ipynb) and, where applicable, from the enrichment script in [`run_GO.R`](../scripts/r/run_GO.R).

```bash
python -m jupyter nbconvert --to notebook --execute \
  workflow/scripts/notebooks/Remake_Plots.ipynb --inplace

Rscript workflow/scripts/r/run_GO.R
```

## Results Summary
<!-- Record the main findings from the follow-up analyses. -->

The follow-up analysis `[confirmed / refined / weakened / extended]` the interpretation from the main workflow. Using `[fill in new threshold, plot remake, subgroup, or comparison set]` resulted in `[fill in key change in findings / no material change in interpretation / a more focused view of the same signal]`.

<!-- (examples)
- Follow-up comparisons with the strongest additional signal: `[fill in or remove bullet]`
- Whether the follow-up changed the main project interpretation: `[fill in or remove bullet]`
- Any output selected for reuse in [final_report](../final_report/README.md): `[fill in or remove bullet]`
-->

## Notes
<!-- Record any changes in thresholds, interpretation, or analysis scope. -->

- Threshold changes from the main workflow: `[fill in or none]`
- Plots or tables remade from [03_visualization](../03_visualization/README.md): `[fill in or none]`
- Follow-up outputs selected for [final_report](../final_report/README.md): `[fill in or remove bullet]`
