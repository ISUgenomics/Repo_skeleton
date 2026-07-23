# 05_Introduction

This file holds project-specific context that can be adapted into an initial draft of the introduction.

- [Manuscript-Style Summary](#manuscript-style-summary)

<!-- Editor guide
Use this file to draft manuscript-style introduction prose from the project background, design, and study aims.

Recommended logic:

1. Start with the biological relevance of the tissue, organism, or system under study.
2. Introduce the main biological or experimental factors and explain why each is relevant.
3. Explain why the selected study design is appropriate for separating the intended effects.
4. Add a short standardized statement describing why proteomics is an appropriate approach in this context.
5. End with a direct study objective or aim sentence aligned with the prespecified comparisons.

Writing guidance:

- Move from broad biological context to the specific study question.
- Keep terminology and group names consistent with the project README and metadata files.
- Keep this section focused on rationale, background, and study aim; do not summarize results here.
- Prefer prose that can be reused in an initial manuscript draft with only minor project-specific adjustment.
-->

## Manuscript-Style Summary

The `{{ tissue_or_material }}` is a biologically informative context for this study. Changes in `{{ tissue_or_material }}` physiology can be reflected at the protein level, making proteomic profiling a useful approach for evaluating how `{{ main_experimental_factors }}` influence this system.

`{{ primary_factor_name }}` was included as a primary design factor. Samples were assigned to `{{ primary_factor_levels }}`, allowing assessment of whether `{{ primary_factor_question }}`. The motivating hypothesis for this project was that `{{ primary_biological_hypothesis }}`.

`{{ secondary_factor_name }}` was examined across `{{ secondary_factor_levels_and_rationale }}`. This contrast helps distinguish proteomic changes associated with `{{ secondary_factor_effect }}` from changes that may arise within `{{ confounding_or_context_factor }}`. The study design also supports evaluation of `{{ interaction_or_context_question }}`.

Untargeted LC-MS/MS proteomics provides a global view of protein abundance patterns in `{{ tissue_or_material }}` and can detect coordinated molecular changes associated with `{{ main_factors }}`. In this study, proteomics was used to assess whether the `{{ tissue_or_material }}` protein profile differed across `{{ prespecified_comparisons_summary }}`.

{{ project_objective_sentence }}
