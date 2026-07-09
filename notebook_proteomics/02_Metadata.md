#### 02_Metadata.md

<!--
Editor notes:
- This file should agree with workflow/00_raw_data/config/sample_metadata.csv and workflow/00_raw_data/config/comparisons.csv.
- Do not define comparisons first in the notebook.
- If sample names change, update every location immediately.

Copy-paste status snippets:
- ⬜ validation pending
- ✅ validation complete
-->

[Experimental Design](#experimental-design)
[Required Metadata Fields](#required-metadata-fields)
[Sample Metadata Table](#sample-metadata-table)
[Comparison Table](#comparison-table)
[Validation Checks](#validation-checks)

---

- **Date created:** [YYYY-MM-DD]
- **Last updated:** [YYYY-MM-DD]

## Experimental Design

> [REQUIRED: brief summary of sample layout and factors]

## Required Metadata Fields

Minimum required columns in `sample_metadata.csv`:

| Column | Required | Description |
|--------|----------|-------------|
| `sample_id` | yes | final short sample name used in plots and matrices |
| `source_column` | yes | original column name from provider export |
| `group` | yes | primary grouping used in comparisons |
| `replicate` | yes | biological or technical replicate id |
| `batch_or_run` | yes | run, fraction, plate, or batch field |
| `include` | yes | `TRUE/FALSE` flag for analysis inclusion |
| `notes` | no | special handling notes |

Add project-specific columns as needed, for example `tissue`, `timepoint`, `treatment`, `animal_id`, `fraction`, `sex`, or `dose`.

## Sample Metadata Table

| sample_id | source_column | group | replicate | batch_or_run | include | notes |
|-----------|---------------|-------|-----------|--------------|---------|-------|
| `[REQUIRED]` | `[REQUIRED]` | `[REQUIRED]` | `[REQUIRED]` | `[REQUIRED]` | `TRUE` | |

## Comparison Table

| comparison_id | group1 | group2 | use_qvalue | pvalue_cutoff | qvalue_cutoff | abs_log2fc_cutoff | enabled |
|---------------|--------|--------|------------|---------------|---------------|-------------------|---------|
| `[REQUIRED]` | `[REQUIRED]` | `[REQUIRED]` | `TRUE` | `0.05` | `0.05` | `1` | `TRUE` |

## Validation Checks

- ⬜ every `source_column` exists in the provider export
- ⬜ every `sample_id` is unique
- ⬜ every enabled comparison has at least 3 samples per group, or the exception is documented
- ⬜ excluded samples are flagged explicitly and explained
- ⬜ notebook uses these tables instead of hardcoded group lists
