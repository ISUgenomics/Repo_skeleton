<!-- Editor notes:
- Keep rendered content concise and project-facing.
- Use workflow/ as the live execution workspace and root numbered files as summary/manuscript-facing documents.
- Fill config files and workflow records with project facts from the actual run.

Copy-paste status snippets:
- ⬜ not started
- ✅ done
- [ ] markdown unchecked task
- [x] markdown checked task
-->

# Proteomics Project

- [How to use this template](#how-to-use-this-template)
- [Environment setup](#environment-setup)
- [Required project-specific inputs](#required-project-specific-inputs)
- [Project structure for proteomics analysis](#project-structure-for-proteomics-analysis)
- [Documentation for manuscript writing](#documentation-for-manuscript-writing)

The `notebook_proteomics/` template is a documentation-first scaffold for standardized proteomics analysis. It keeps the manuscript-supporting `.md` files at the project root and uses `workflow/` as the real execution workspace: live process notes, decision points, issues, intermediate outputs, and analysis results.

```bash
notebook_proteomics/
├── *.md              # see Documentation for manuscript writing
└── workflow/         # see Project structure for proteomics analysis 
```

## How to use this template

1. Copy `notebook_proteomics/` into a new project repository.
2. Create the analysis environment from `environment.yml` or `requirements.txt`.
3. Start in `workflow/00_raw_data/`, place or document the provider export, and record any optional cleanup there.
4. Fill `workflow/00_raw_data/config/project_manifest.yaml`, `sample_metadata.csv`, and `comparisons.csv`.  
  If helpful, bootstrap config with:
```bash
python workflow/scripts/python/bootstrap_config.py \
  --project-root . \
  --input-file workflow/00_raw_data/<provider_export>.xlsx \
  --legacy-metadata workflow/00_raw_data/<metadata.txt_or_xlsx>
```

5. Follow the numbered workflow steps and record commands, outputs, observations, and issues as the analysis progresses.
6. Run `workflow/scripts/notebooks/proteomics_analysis.ipynb` only after the config files are final.
7. Use `workflow/scripts/notebooks/Remake_Plots.ipynb` only for follow-up or alternate-threshold plotting when needed.
8. Update root `.md` files as the project progresses.


## Environment setup

Two environment files are provided at the project root:

| File | Use |
|------|-----|
| `environment.yml` | preferred Conda environment |
| `requirements.txt` | `venv` / `pip` environment |

Conda:

```bash
conda env create -f environment.yml
conda activate notebook_proteomics
```

venv:

```bash
python3 -m venv .venv
. .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

Important dependency notes:

- `openpyxl` is required for the current Excel-based raw data exports to pipeline config.
- Plotly static `PNG`/`SVG` export currently depends on Kaleido plus a working native Chrome or Chromium installation.
- If no compatible browser is available, the plotting scripts still write HTML outputs and skip static export with a warning.

<details><summary><i>Optional Linux or HPC workaround for PNG/SVG figure export</i></summary>

If static Plotly export fails on Linux because no usable Chrome or Chromium is available in the runtime environment, a user-space Chromium install can be used without changing the pipeline defaults.

Validated Ubuntu `arm64` recipe:

```bash
python -m venv .venv
.venv/bin/pip install -r requirements.txt
.venv/bin/pip install playwright
.venv/bin/python -m playwright install chromium
sudo apt-get update
sudo apt-get install -y \
  libnspr4 libnss3 libatk1.0-0t64 libatk-bridge2.0-0t64 libcups2t64 \
  libxcb1 libxkbcommon0 libasound2t64 libgbm1 libx11-6 libxext6 \
  libcairo2 libpango-1.0-0 libxcomposite1 libxdamage1 libxfixes3 \
  libxrandr2 libatspi2.0-0t64
```

If Plotly or Kaleido still prefers a broken browser previously downloaded by `plotly_get_chrome` or `choreo_get_chrome`, point the local choreographer browser path at the working Chromium binary for that environment. In the Ubuntu validation environment, the working override was:

```bash
mv ~/.local/share/choreographer/deps/chrome-linux64/chrome \
   ~/.local/share/choreographer/deps/chrome-linux64/chrome.x86_backup
ln -s ~/.cache/ms-playwright/chromium-*/chrome-linux/chrome \
   ~/.local/share/choreographer/deps/chrome-linux64/chrome
```

This is an environment-level workaround for Linux systems that do not already provide a working native browser. On macOS and standard desktop setups, prefer the system Chrome or Chromium installation and avoid custom overrides unless static export fails.
</details>


## Required project-specific inputs

These files must be completed before analysis:

| File | Purpose |
|------|---------|
| `workflow/00_raw_data/config/project_manifest.yaml` | one source of truth for project id, paths, notebook name, data type, normalization choices |
| `workflow/00_raw_data/config/sample_metadata.csv` | sample-level metadata used for grouping, plotting, and table generation |
| `workflow/00_raw_data/config/comparisons.csv` | all requested comparisons and thresholds |

Guides:
- `workflow/00_raw_data/README.md` - raw data intake notes and optional preprocessing record 
- `workflow/scripts/README.md` - index of actual scripts present in `workflow/scripts/` 


## Project structure for proteomics analysis

The `workflow/` folder is meant to be the active analysis worktree. The root numbered `.md` files remain project-summary and publication-facing documents.

```text
workflow/
├── 00_raw_data/              # starting point: raw data (xlsx), pipeline config, notes
│   └── config/               # project manifest, metadata, and comparison definitions
├── 01_qc_normalization/      # PRTC checks, normalization diagnostics, normalized matrices
├── 02_statistics/            # per-comparison tests and result tables
├── 03_visualization/         # volcano, heatmap, PCA, PLS-DA notes and output/
├── 04_secondary_analyses/    # extra comparison sets & plots, project-specific follow-up
├── final_report/             # compiled result narrative and manuscript-facing figures
└── scripts/                  # reusable scripts, helpers, and execution notebooks
```


## Documentation for manuscript writing

| File | Phase | Description |
|------|-------|-------------|
| `00_Background.md` | project | project context, aims, collaborators, decisions |
| `01_Files.md` | analysis | source files, exports, locations, expected outputs |
| `02_Metadata.md` | analysis | sample metadata, grouping rules, comparison design |
| `03_Methods.md` | analysis | experimental and computational methods |
| `04_Results.md` | analysis | summary of QC, normalization, statistics, plots |
| `05_Introduction.md` | paper | manuscript introduction draft |
| `06_Discussion.md` | paper | manuscript discussion draft |
| `07_Supplementary.md` | paper | optional extra figures, comparisons, notes |
| `08_References.md` | paper | methods and manuscript references |
| `09_AuthorInfo.md` | paper | authors, affiliations, funding, acknowledgments |
| `README.md` | general | overview of the template and expected workflow |
| `othernotes.md` | general | scratchpad for unresolved notes and follow-up items |
