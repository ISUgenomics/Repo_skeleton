<!--
Editor notes:
- Start this file by documenting the exact source files used for the project.
- Keep visible content factual and tied to the actual input files used in the run.
- If no preprocessing was needed, keep that explicit rather than leaving the section ambiguous.
-->
# 00_raw_data

Raw data and project intake record.

*This step documents the source files and starting data used for the proteomics analysis. It captures what was received, what was cleaned or retained, and which project-specific inputs were carried into the downstream workflow.*

## Input Files
<!-- Report the exact source files used to start the analysis. -->

Input files used to start this proteomics analysis:

| Item | Value |
|------|-------|
| Provider export file | `[fill in]` |
| Original format | `[fill in]` |
| Raw data location | `[fill in]` |
| Source metadata file | `[fill in or remove row]` |
| Project manifest used for this run | [`config/project_manifest.yaml`](./config/project_manifest.yaml) |
| Sample metadata used for this run | [`config/sample_metadata.csv`](./config/sample_metadata.csv) |
| Comparison definitions used for this run | [`config/comparisons.csv`](./config/comparisons.csv) |
| Cleaned export used for analysis | `[fill in or remove row]` |

## Notes
<!-- Note any facts about hidden rows, hidden columns, filtered views, or file preparation. -->

Data intake notes for this project:

The raw intake files for this project consisted of `[fill in source files]`. The starting dataset was `[used as provided / exported as visible-only rows and columns / cleaned before downstream use]`.

- Hidden rows removed: `[yes/no]`
- Hidden columns removed: `[yes/no]`
- Visible-only export used: `[yes/no]`
- Sample naming matched [`config/sample_metadata.csv`](./config/sample_metadata.csv): `[yes/no]`
- Comparison groups required for [`config/comparisons.csv`](./config/comparisons.csv) were present in the source data: `[yes/no]`
- Additional intake notes: `[fill in or remove bullet]`

## Optional Preprocessing
<!-- Use this section only if the source file was cleaned or transformed before the main notebook. -->

Preprocessing applied before the main proteomics workflow:

| Done | Step | Notes |
|------|------|-------|
| `[ ]` | No preprocessing required | |
| `[ ]` | Visible-only export created | |
| `[ ]` | Sample names standardized | |
| `[ ]` | Annotation fields standardized | |
| `[ ]` | Abundance or identifier columns renamed | |
| `[ ]` | Non-data rows removed | |
| `[ ]` | Other preprocessing step | `[fill in or remove row]` |

## Execution
<!-- Paste the commands used or briefly describe the manual actions taken. -->

Commands or manual actions used during intake and preprocessing:

```bash
[paste commands or describe manual actions here]
```

## Final File Passed to Analysis
<!-- Record the exact filename passed to the downstream notebook or script. -->

Final file passed to [01_qc_normalization](../01_qc_normalization/README.md): `[fill in]`
