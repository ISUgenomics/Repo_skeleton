<!--
Editor notes:
- This file documents optional documentation helpers only.
- Keep examples aligned with actual helper arguments and output filenames.
-->
# docs

Documentation helper scripts for the proteomics workflow.

These helpers are optional. They read workflow outputs and write structured JSON summaries that can be used for report autofill, downstream validation, or manual project review.

Run them from the project root unless you provide absolute paths.

Additional project-context files may be placed in `workflow/00_raw_data/`, preferably as plain `*.txt` files such as:

- `correspondence.txt`
- `summary.txt`
- `biological_question.txt`

When present, `extract_project_context.py` will read those files, convert recognized content into structured context fields, and preserve each text file as a flat `text_context_<file_stem>` value for downstream documentation autofill.

For correspondence-like text files, the helper can also parse simple mail-style headers such as:

- `From:`
- `Date:`
- `To:`
- `Cc:`
- `Subject:`

Those headers can be used to infer project contacts, analysis contacts, facility names, and key-correspondence fields when the project provides them in plain text.

The same blob may also include simple section headings for manuscript-support fields, for example:

- `Authors:`
- `Affiliations:`
- `Contributions:`
- `Funding:`
- `Acknowledgements:`
- `System or tissue references:`
- `Condition or treatment references:`
- `Project-specific references:`
- `Local relevant references:`
- `References:`

When those sections are present, the helper will extract them into the corresponding documentation variables. When they are absent, it falls back only to conservative inference from the available contact and facility context.

## Available Helpers

| Script | Purpose | Inputs | Outputs |
|--------|---------|--------|---------|
| [`common.py`](./common.py) | Shared lightweight parsers and JSON helpers used by the other extractors | config files, CSV outputs | reusable helper functions |
| [`extract_project_context.py`](./extract_project_context.py) | Summarize project context from manifest, metadata, and additional `workflow/00_raw_data/*.txt` files | manifest, metadata summary, optional `.txt` files | `project_context.json` |
| [`extract_metadata_summary.py`](./extract_metadata_summary.py) | Summarize sample groups, factor levels, and enabled comparisons | `sample_metadata.csv`, `comparisons.csv` | `metadata_summary.json` |
| [`extract_statistics_summary.py`](./extract_statistics_summary.py) | Summarize per-comparison hit counts, fold-change direction balance, and example hits | `workflow/02_statistics/CSV/*.csv`, `significant_protein_counts.csv` | `statistics_summary.json` |
| [`extract_visualization_inventory.py`](./extract_visualization_inventory.py) | Check expected plot families and formats for each enabled comparison | `comparisons.csv`, visualization output folders | `visualization_inventory.json` |
| [`extract_significant_hits.py`](./extract_significant_hits.py) | Extract significant-hit tables from per-comparison statistics CSVs | `workflow/02_statistics/CSV/*.csv` | `significant_hits_summary.json` |
| [`extract_results_report_fields.py`](./extract_results_report_fields.py) | Convert structured summaries into flat report-ready result variables | metadata, statistics, visualization, and hit-summary JSONs | `results_report_fields.json` |
| [`extract_execution_report_fields.py`](./extract_execution_report_fields.py) | Convert execution summaries into flat workflow-step status and note fields | project context, metadata, statistics, visualization, and run summary JSONs | `execution_report_fields.json` |
| [`extract_run_summary.py`](./extract_run_summary.py) | Combine manifest, metadata, statistics, visualization, and software-version summaries into one compact run summary | manifest, helper JSON summaries, software versions | `run_summary.json` |

## Typical Usage

Generate metadata and comparison summary:

```bash
python3 workflow/scripts/python/docs/extract_project_context.py
```

```bash
python3 workflow/scripts/python/docs/extract_metadata_summary.py
```

Generate statistics summary:

```bash
python3 workflow/scripts/python/docs/extract_statistics_summary.py
```

Generate visualization inventory:

```bash
python3 workflow/scripts/python/docs/extract_visualization_inventory.py
```

Generate significant-hit summary:

```bash
python3 workflow/scripts/python/docs/extract_significant_hits.py
```

Generate report-ready result fields:

```bash
python3 workflow/scripts/python/docs/extract_results_report_fields.py
```

Generate workflow-step report fields:

```bash
python3 workflow/scripts/python/docs/extract_execution_report_fields.py
```

Generate combined run summary:

```bash
python3 workflow/scripts/python/docs/extract_run_summary.py
```

## Custom Paths

If needed, run a helper against explicit files:

```bash
python3 workflow/scripts/python/docs/extract_project_context.py \
  --manifest-file workflow/00_raw_data/config/project_manifest.yaml \
  --metadata-summary workflow/scripts/python/docs/metadata_summary.json \
  --raw-data-dir workflow/00_raw_data \
  --output-dir workflow/scripts/python/docs
```

```bash
python3 workflow/scripts/python/docs/extract_metadata_summary.py \
  --metadata-file workflow/00_raw_data/config/sample_metadata.csv \
  --comparisons-file workflow/00_raw_data/config/comparisons.csv \
  --output-dir workflow/scripts/python/docs
```

```bash
python3 workflow/scripts/python/docs/extract_statistics_summary.py \
  --stats-dir workflow/02_statistics/CSV \
  --counts-file workflow/02_statistics/significant_protein_counts.csv \
  --output-dir workflow/scripts/python/docs
```

```bash
python3 workflow/scripts/python/docs/extract_visualization_inventory.py \
  --comparisons-file workflow/00_raw_data/config/comparisons.csv \
  --output-root workflow/03_visualization/output \
  --output-dir workflow/scripts/python/docs
```

```bash
python3 workflow/scripts/python/docs/extract_significant_hits.py \
  --input-dir workflow/02_statistics/CSV \
  --output-dir workflow/scripts/python/docs
```

```bash
python3 workflow/scripts/python/docs/extract_results_report_fields.py \
  --metadata-summary workflow/scripts/python/docs/metadata_summary.json \
  --statistics-summary workflow/scripts/python/docs/statistics_summary.json \
  --visualization-summary workflow/scripts/python/docs/visualization_inventory.json \
  --significant-hits-summary workflow/scripts/python/docs/significant_hits_summary.json \
  --output-dir workflow/scripts/python/docs
```

```bash
python3 workflow/scripts/python/docs/extract_execution_report_fields.py \
  --project-context workflow/scripts/python/docs/project_context.json \
  --metadata-summary workflow/scripts/python/docs/metadata_summary.json \
  --statistics-summary workflow/scripts/python/docs/statistics_summary.json \
  --visualization-summary workflow/scripts/python/docs/visualization_inventory.json \
  --run-summary workflow/scripts/python/docs/run_summary.json \
  --output-dir workflow/scripts/python/docs
```

```bash
python3 workflow/scripts/python/docs/extract_run_summary.py \
  --manifest-file workflow/00_raw_data/config/project_manifest.yaml \
  --metadata-summary workflow/scripts/python/docs/metadata_summary.json \
  --statistics-summary workflow/scripts/python/docs/statistics_summary.json \
  --visualization-summary workflow/scripts/python/docs/visualization_inventory.json \
  --software-versions workflow/01_qc_normalization/software_versions.txt \
  --output-dir workflow/scripts/python/docs
```

## Notes

- These helpers are intended to read existing workflow outputs; they do not replace the main notebook run.
- If a required upstream output is missing, the corresponding JSON fields may remain empty or partial.
- The template contract can declare these helpers in `template/executor.yaml` so they run automatically after the main workflow completes.
