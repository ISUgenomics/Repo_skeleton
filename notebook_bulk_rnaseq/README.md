# Bulk RNA-Seq Project 

- [Documentation for easy manuscript writing](#documentation-for-easy-manuscript-writing)
- [Project Structure for bulk RNA-Seq computations](#project-structure-for-bulk-rna-seq-computations)
- [How to use this template?](#how-to-use-this-template)
  - [Copy the file structure](#copy-the-file-structure)


The **notebook_bulk_rnaseq/** template provides high-level `.md` files for summarizing the project, interpreting results and facilitating manuscript preparation, while the **workflow/** folder captures detailed, step-by-step documentation and progress tracking for the computational steps in the pipeline.

```text
notebook_bulk_rnaseq/
├── *.md
└── workflow/
```

## Documentation for easy manuscript writing

Each `.md` file in the root directory is intended to support scientific reporting and manuscript drafting. These documents allow you to record key metadata, summarize decisions and methods and organize insights for publication.

| File                  | Phase      | Description                                                                         |
|-----------------------|------------|-------------------------------------------------------------------------------------|
| 00_Background.md      | project    | project background: goals, aims, biological question, collaborators, contacts       |
| 01_Files.md           | analysis   | list of raw and processed data files (and location) used in the project             |
| 02_Metadata.md        | analysis   | metadata tables: sample annotations, clinical info, experimental design             |
| 03_Methods.md         | analysis   | detailed experimental and computational methods; tools/steps selected in a pipeline |
| 04_Results.md         | analysis   | per step results summary, figures, tables and main findings                         |
| 05_Introduction.md    | paper      | manuscript introduction section                                                     |
| 06_Discussion.md      | paper      | manuscript discussion section                                                       |
| 07_Supplementary.md   | paper      | (optional) supplementary results, extended figures and additional methods           |
| 08_References.md      | paper      | bibliography and references; defaults for methods pre-filled                        |
| 09_AuthorInfo.md      | paper      | author list, contributions, affiliations                                            |
| 10_Acknowledgements.md| paper      | acknowledgements: funding, grants, institutional support, thanks                    |
| **README.md**         | general    | (this file) overview of the template and how to use it; project structure           |
| othernotes.md         | general    | scratchpad for miscellaneous notes, ideas and to-dos                                |


## Project Structure for bulk RNA-Seq computations

The [**workflow/**](workflow/) folder provides a structured project layout for performing **bulk RNA-seq analysis**, from raw data acquisition to statistical modeling and reporting. It is intended to document your progress during computational analysis, including decision point, issues and troubleshooting. This promotes reproducibility, consistency and documentation across all stages of the pipeline.

```bash
workflow/                         # root folder for your RNA-Seq project; customize it
├── 00_raw_data/                  # raw FASTQ files, md5 checksums
├── 01_read_qc/                   # fastqc reports, multiqc summary
├── 02_trimming/                  # trimmed FASTQs, trimming logs (optional)
├── 03_alignment/                 # bam/cram alignments, indexes (optional)
│   ├── ref_assembly/             # reference genome or transcriptome (downloaded or assembled de novo)
│   └── <align_tool>              # e.g, star, hisat2, minimap2 for the alignment step
├── 04_quantification/            # count matrices or quant.sf files
├── 05_dge/                       # differential expression analysis
│   ├── 0-config/                 # contrasts, covariates, sample groups
│   ├── 1_analysis/               # DE testing (deseq2/edger/limma)
│   ├── 2_downstream/             # functional/enrichment analyses (GO, KEGG, pathways, networks)
│   └── 3_plots/                  # pca, ma-plots, volcano, heatmaps
├── 06_ase/                       # allele-specific expression (optional)
│   ├── 0-config/                 # vcf/cram paths, phasing info, filters
│   ├── 1_analysis/               # ASE quantification + tests
│   ├── 2_annotation/             # imprinting, eQTL overlap, gene sets
│   └── 3_plots/                  # per-gene tables, imbalance plots, summary md 
├── 07_fusion_detection/          # fusion transcript detection (optional)
│   ├── 0-config/                 # reference, filters (read support, blacklist)
│   ├── 1_analysis/               # star-fusion/arriba/fusioncatcher outputs
│   ├── 2_annotation/             # cosmic annotation, oncogenic pathways, domain/partner checks
│   └── 3_plots/                  # sashimi-like visuals, oncoplots, summary md
└── final_report/                 # compiled report, EDA, figures/tables for manuscript
```

## How to use this template?

1. [Copy this template folder](#copy-the-file-structure) into your new project folder or Git repository.
2. Navigate to [workflow/README.md](workflow/README.md) to select the analysis steps you plan to perform. *(Remove unused folders.)*
3. Fill in the documentation files (`*.md`) progressively during the project.

### Copy the file structure

To initialize your own project with this template structure:

**Option 1: Download from GitHub**

1. Navigate to the [`Repo_skeleton/notebook_bulk_rnaseq/`](https://github.com/ISUgenomics/Repo_skeleton/tree/main/notebook_bulk_rnaseq) folder on GitHub.
2. Click the green **“Code”** button → **“Download ZIP”**.
3. Extract the ZIP file and move the `notebook_bulk_rnaseq/` folder into your project directory.
4. You can rename the folder, if needed.

**Option 2: Clone only the subdirectory**

If you're comfortable with Git:

```bash
git clone --filter=blob:none --sparse https://github.com/ISUgenomics/Repo_skeleton.git
cd Repo_skeleton
git sparse-checkout set notebook_bulk_rnaseq
mv notebook_bulk_rnaseq/ ../your_project/
cd ..
rm -rf Repo_skeleton
```
Now you have just the **notebook_bulk_rnaseq/** folder in your project. You can rename the folder, if needed. 