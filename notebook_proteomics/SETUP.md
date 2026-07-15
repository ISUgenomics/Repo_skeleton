<!-- Editor notes:
- Keep rendered content concise and project-facing.
- Use workflow/ as the live execution workspace. Fill workflow/config/ files with project facts from the actual run. 
-->

# SETUP

- [How to use this template](#how-to-use-this-template)

The `notebook_proteomics/` template is a documentation-first scaffold for standardized proteomics analysis. It keeps the manuscript-supporting `.md` files at the project root and uses `workflow/` as the real execution workspace: live process notes, decision points, issues, intermediate outputs, and analysis results.

```bash
notebook_proteomics/
├── workflow/         # see steps 3 to 6 - analysis
└── *.md              # see step 7 - documentation
```

The `workflow/` folder is meant to be the active analysis worktree.

```bash
workflow/
├── 00_raw_data/              # starting point: raw data (xlsx) and metadata
│   └── config/               # pipeline settings, treatments, and comparison definitions
├── 01_qc_normalization/      # PRTC checks, normalization diagnostics, normalized matrices
├── 02_statistics/            # per-comparison tests and result tables
├── 03_visualization/         # volcano, heatmap, PCA, PLS-DA notes and output/
├── 04_secondary_analyses/    # extra comparison sets & plots, project-specific follow-up
├── final_report/             # compiled result narrative and manuscript-facing figures
└── scripts/                  # reusable scripts, helpers, and execution notebooks
```

## How to use this template

*(Full Guide)*

<details><summary>1. Copy <b>notebook_proteomics/</b> template into your project's repo.</summary>

Create a new repository in the GitHub UI with a simple `README.md` that gives a one-sentence description of the project.

Then clone it to your local machine and copy only the contents of `notebook_proteomics/` into that repository, not the parent folder itself.

```bash
git clone <your-github-repo-url>
cd <your-repo-name>
cp -R /path/to/notebook_proteomics/. .
```

</details>

<details><summary>2. Create the <b>environment</b> for the analysis.</summary>

Two environment files are provided at the project root:

<details><summary><i>environment.yml</i> - preferred <b>conda</b> environment</summary>

```bash
conda env create -f environment.yml
conda activate proteomics
python -m ipykernel install --user --name proteomics --display-name "Python (proteomics)"
```

If you want VS Code, JupyterLab, or classic Jupyter Notebook to show the environment as a notebook kernel, run the `ipykernel install` command once after activating the environment.
</details>

<details><summary><i>requirements.txt</i> - preferred <b>venv</b> or <b>pip</b> environment</summary>

```bash
python3 -m venv .venv
. .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
python -m ipykernel install --user --name notebook_proteomics_venv --display-name "Python (notebook_proteomics_venv)"
```

If you use the `venv` route, the `ipykernel install` command makes that environment selectable from `Select Kernel` in VS Code and from the kernel picker in Jupyter.
</details>

---

After creating either environment, verify that notebook launchers can see it:

- VS Code: open the notebook, click `Select Kernel`, and choose `Python (proteomics)` or `Python (notebook_proteomics_venv)`.
- JupyterLab or classic Notebook: start Jupyter from the activated environment and select the matching kernel name in the notebook UI.

---

Important dependency notes:

- `openpyxl` is required for the current Excel-based raw data exports to pipeline config.
- Plotly static `PNG`/`SVG` export currently depends on Kaleido plus a working native Chrome or Chromium installation. If no compatible browser is available, the plotting scripts still write interactive HTML outputs and skip static export with a warning.

<details style="margin-left: 25px;"><summary><i>Optional Linux or HPC workaround for PNG/SVG figure export</i></summary>

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

</details>

<details><summary>3. Put <b>raw data</b> and any <b>metadata</b> source files in <code>workflow/00_raw_data/</code>.</summary>

Guides:
- `workflow/00_raw_data/README.md` - raw data intake notes and optional preprocessing record 


</details>

<details><summary>4. Generate <b>config</b> (settings, treatments, comparisons) for the analysis.</summary>

The `workflow/00_raw_data/config/` folder stores files used to start and control the proteomics analysis:

| File | Purpose |
|------|---------|
| `project_manifest.yaml` | minimal startup settings for the notebook: project details, raw data file, and key analysis options |
| `sample_metadata.csv` | sample information used to define groups and connect sample names to the data file; created by the notebook if missing |
| `comparisons.csv` | list of comparisons to run; created by the notebook if missing |

Recommended setup order:
  1. place raw data and any metadata source file in `workflow/00_raw_data/`
  2. run `config_gen.py` [[Manifest - analysis settings](#manifest---analysis-settings)]
  3. review and correct `project_manifest.yaml`
  4. run `metadata_gen.py` [[Sample treatments and comparisons](#sample-treatments-and-comparisons)]
  5. review or correct `sample_metadata.csv` and `comparisons.csv`
  6. launch the notebook

### Manifest - analysis settings

Use `config_gen.py` to auto-create `project_manifest.yaml` from the current project structure.</summary>

```bash
python workflow/scripts/python/config_gen.py --project-root .
```
*Use `--force` to overwrite an existing `project_manifest.yaml`.*

**Always review and correct the generated values before running the analysis.**

<details style="margin-left: 20px;"><summary>IMPORTANT: astral_mode for "zero" values handling</summary>

`config_gen.py` estimates `analysis.astral_mode` automatically from the raw data when possible. The template still defaults toward `true` because most grouped-abundance exports used with this workflow come from the same source pattern and often behave like zeros are missing-value placeholders.

Optionally, use `infer_astral_mode.py` immediately after `config_gen.py` if you want the reasoning summary before keeping or changing the generated value.

```bash
python workflow/scripts/python/infer_astral_mode.py \
  --manifest workflow/00_raw_data/config/project_manifest.yaml
```

If the helper recommendation disagrees with the current manifest value, update `analysis.astral_mode` before running the notebook.

</details>

### Sample treatments and comparisons 

Run `metadata_gen.py` to create or validate `sample_metadata.csv` and `comparisons.csv`
- after `project_manifest.yaml` exists and has been reviewed, 
- and before notebook or CLI-based analysis execution.

```bash
python workflow/scripts/python/metadata_gen.py --manifest workflow/00_raw_data/config/project_manifest.yaml
```

If a raw metadata_source file is available in `workflow/00_raw_data/`, `metadata_gen.py` can often infer the header row and common mappings automatically. Use explicit selectors only when the file layout is unusual or the inferred mapping needs correction.

```bash
python workflow/scripts/python/metadata_gen.py \
  --manifest workflow/00_raw_data/config/project_manifest.yaml \
  --input "workflow/00_raw_data/metadata_source.xlsx" \
  --header 2 \
  --sample sample_id \
  --treatment treatment \
  --factor challenge=challenge \
  --group group
```

- Use `--force` to overwrite existing `sample_metadata.csv` and auto-generated `comparisons.csv`.  
- Use `--no-comparisons` if you only want `sample_metadata.csv`.  
- See `workflow/scripts/README.md` for more details.

---

Unless user-provided, `sample_metadata.csv` and `comparisons.csv` are auto-created from the detected sample columns in the raw data file. If `sample_metadata.csv` already exists before notebook launch, the notebook follows the validation-first path instead of creating a blank starter template.

`sample_metadata.csv` template:
```csv
sample_id,source_column,treatment,group,replicate,batch_or_run,include,notes
fill_in_sample_01,fill_in_source_column_01,fill_in_treatment,fill_in_group,1,fill_in_run,TRUE,
```

`comparisons.csv` template:
```csv
comparison_id,grouping_column,group1,group2,use_qvalue,pvalue_cutoff,qvalue_cutoff,abs_log2fc_cutoff,enabled,notes
fill_in_comparison_01,fill_in_grouping_column,fill_in_group_a,fill_in_group_b,TRUE,0.05,0.05,1,TRUE,
```

<details style="margin-left: 20px;"><summary>IMPORTANT! Behavior notes</summary>

- `sample_metadata.csv` is validated against the raw data file so each `source_column` must match a real sample-abundance column after renaming.
- Any `--factor name=...` field becomes a real metadata column and can be used later in `comparisons.csv`.
- `comparisons.csv` is validated against `sample_metadata.csv` so each `grouping_column`, `group1`, and `group2` must resolve to defined metadata values.
- You can limit expected comparisons by editing `comparisons.csv` before or after auto-creation: disable rows with `enabled=FALSE`, delete unneeded rows, or provide only the specific comparisons you want to run.
- Provided comparison definitions are automatically checked for compatibility with the dataset before downstream statistics and plotting.
- `project_manifest.yaml -> inputs.comparisons_mode` controls whether `comparisons.csv` is workflow-generated or treated as a manual curated file. Use `generated` to allow regeneration from corrected metadata, or `manual` to preserve the file on disk and only validate it.
</details>

</details>


<details><summary>5. Launch a ready-made <b>notebook</b> and execute the workflow.</summary>

Launch the analysis notebook located in [`workflow/scripts/notebooks/proteomics_analysis.ipynb`](./workflow/scripts/notebooks/proteomics_analysis.ipynb) in your preferred development environment.

<details style="margin-left: 20px;"><summary><i>VS Code</i></summary>

Open the copied project folder in VS Code, then open [`workflow/scripts/notebooks/proteomics_analysis.ipynb`](./workflow/scripts/notebooks/proteomics_analysis.ipynb).

- Select the project Python interpreter or kernel from the environment you created for this template.
- Run the notebook from top to bottom after confirming the manifest, raw data file path, and any user-provided `sample_metadata.csv` or `comparisons.csv`.
- Review any auto-created `workflow/00_raw_data/config/sample_metadata.csv` and `workflow/00_raw_data/config/comparisons.csv`, correct them if needed, then re-run the notebook from the top.

</details>

<details style="margin-left: 20px;"><summary><i>JupyterLab</i></summary>

From the copied project root:

```bash
jupyter lab
```

Then open [`workflow/scripts/notebooks/proteomics_analysis.ipynb`](./workflow/scripts/notebooks/proteomics_analysis.ipynb), choose the correct kernel, and run cells in order from top to bottom. If the notebook creates starter `sample_metadata.csv` or `comparisons.csv`, stop after creation, review those files, then restart and run the notebook again from the beginning.

</details>

<details style="margin-left: 20px;"><summary><i>Classic Jupyter Notebook</i></summary>

From the copied project root:

```bash
jupyter notebook
```

Then open [`workflow/scripts/notebooks/proteomics_analysis.ipynb`](./workflow/scripts/notebooks/proteomics_analysis.ipynb), select the project kernel, and execute the notebook in order. Use the same review step for any auto-created config CSVs before treating the run as final.

</details>

<details style="margin-left: 20px;"><summary><i>CLI-based workflow execution</i></summary>

If you prefer command-line execution instead of the notebook (e.g., using HPC infrastructure), the script inventory and execution order are summarized in [`workflow/scripts/README.md`](./workflow/scripts/README.md).

Minimal command-line run order includes:

```bash
python workflow/scripts/python/filter_and_Normalize.py run \
  --manifest workflow/00_raw_data/config/project_manifest.yaml

python workflow/scripts/python/Stats.py run \
  --manifest workflow/00_raw_data/config/project_manifest.yaml

python workflow/scripts/python/volcano_plotter.py \
  --input workflow/02_statistics/CSV/<group1>_vs_<group2>_comparison.csv \
  --output-dir workflow/03_visualization \
  --pvalue-limit 0.05 \
  --qvalue-limit 0.05 \
  --fold-change-limit 1

python workflow/scripts/python/heatmap_plotter.py \
  --input workflow/02_statistics/CSV/<group1>_vs_<group2>_comparison.csv \
  --metadata workflow/00_raw_data/config/sample_metadata.csv \
  --grouping-column group \
  --group1 <group1> \
  --group2 <group2> \
  --output-dir workflow/03_visualization \
  --pvalue-limit 0.05 \
  --qvalue-limit 0.05 \
  --fold-change-limit 1

python workflow/scripts/python/pca_plotter.py \
  --input workflow/01_qc_normalization/normalized_abundance_matrix.csv \
  --metadata workflow/00_raw_data/config/sample_metadata.csv \
  --grouping-column group \
  --group1 <group1> \
  --group2 <group2> \
  --output-dir workflow/03_visualization
```

For exact per-step command context and output expectations, see:

- [`workflow/01_qc_normalization/README.md`](./workflow/01_qc_normalization/README.md)
- [`workflow/02_statistics/README.md`](./workflow/02_statistics/README.md)
- [`workflow/03_visualization/README.md`](./workflow/03_visualization/README.md)

</details>

</details>

<details><summary>6. (optional) Use Remake_Plots.ipynb only if you need <b>follow-up plots</b>.</summary>



</details>

<details><summary>7. Update the <b>documentation</b> (*.md files) as the project progresses.</summary>

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
| `README.md` | general | project overview, high-level study summary, and navigation |
| `SETUP.md` | general | setup and execution guide for the analysis executor |
| `othernotes.md` | general | scratchpad for unresolved notes and follow-up items |

</details>


### Quick Steps

Assuming:
- the raw data `.xlsx` file is already in `workflow/00_raw_data/`
- the metadata source file is already in `workflow/00_raw_data/`
- you are in the project's root

Create Conda environment:
```bash
conda env create -f environment.yml
conda activate proteomics
python -m ipykernel install --user --name proteomics --display-name "Python (proteomics)"
```

Generate config for the analysis: 
```bash
python workflow/scripts/python/config_gen.py --project-root .
```

Adjust explicit column mapping to your metadata source file:

```bash
python workflow/scripts/python/metadata_gen.py \
  --manifest workflow/00_raw_data/config/project_manifest.yaml \
  --input "workflow/00_raw_data/metadata_source.xlsx" \
  --header 2 \
  --sample sample_id \
  --treatment treatment \
  --factor challenge=challenge \
  --group group
```

Then open [`workflow/scripts/notebooks/proteomics_analysis.ipynb`](./workflow/scripts/notebooks/proteomics_analysis.ipynb) in VSC or JupyterLab, select `Python (proteomics)` kernel, and run the proteomics analysis.
