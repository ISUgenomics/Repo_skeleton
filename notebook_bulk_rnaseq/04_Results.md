#### 04_Results &emsp; *This document summarizes and organizes key findings from the RNA-seq analysis*

[1. Sample Overview](#1-sample-overview)  
[2. Read Quality and Mapping Summary](#2-read-quality-and-mapping-summary)  
[3. Gene/Transcript Quantification](#3-genetranscript-quantification)  
[4. Differential Expression Analysis](#4-differential-expression-analysis)  
[5. Functional Enrichment Analysis](#5-functional-enrichment-analysis)  
[6. Optional Analyses](#6-optional-analyses-if-applicable)  
  - [a. Transcript/Isoform Analysis](#a-transcriptisoform-analysis)  
  - [b. Allele-Specific Expression](#b-allele-specific-expression)  
  - [c. Fusion Transcript Detection](#c-fusion-transcript-detection)  
[7. Summary Tables & Figures](#7-summary-tables--figures)  

**[Manuscript Results Paragraph](#manuscript-results-paragraph)**  

---

- **Date created:** [YYYY-MM-DD]
- **Last updated:** [YYYY-MM-DD]

---

- Present what was observed, not why it matters - leave interpretation to [06_Discussion.md](06_Discussion.md).
- Be flexible enough to cover both standard and extended analyses (like isoforms or deconvolution).
- For each section, summarize the relevant outputs and perform basic checks for technical correctness.
- Tables and figures are encouraged for clarity. Cross-reference [03_Methods.md](03_Methods.md) for tool details and `/workflow/*/README.md` for execution logs or anomalies.
- Include links to relevant figures in the [07_Supplementary.md](07_Supplementary.md) when appropriate.  
- Use the checklist prompts to verify consistency, detect processing issues, or identify mislabelled samples or bad plots.  
- If a section is not applicable, remove it or mark as *Not performed*.  
- Use the [Manuscript Results Paragraph](#manuscript-results-paragraph) section to begin drafting publication-ready text.

---

Use this file to document and organize results derived from your RNA-seq analysis. Include tables, figures and descriptions as needed. Each subsection reflects a typical component of RNA-seq results. Modify or expand based on your specific study goals and analysis outputs. Summarize statistics objectively.  
Use ✅ checkboxes to mark completed checks.


## 1. Sample Overview

See [workflow/00_raw_data/README.md](workflow/00_raw_data/README.md) for tool logs and command history.  
See [workflow/01_read_qc/README.md](workflow/01_read_qc/README.md) for tool logs and command history.  
See [workflow/02_trimming/README.md](workflow/02_trimming/README.md) for tool logs and command history.  

| Metric                    | Value | cross-link | notes |
|---------------------------|-------|------------|-------|
| Total samples analyzed    | `X`   | [01_Files #Raw Reads RNA](01_Files.md#raw-reads-rna) | |
| Conditions / groups       | `Group A`, `Group B`, ... | [02_Metadata #Sample Grouping](02_Metadata.md#sample-grouping) | |
| Samples excluded          | `Sample_03`  | [workflow/00_raw_data/README](workflow/00_raw_data/README) | low quality |

- ⬜ Do sample counts match metadata?
- ⬜ Are all groups represented evenly?

## 2. Read Quality and Mapping Summary

See [workflow/03_alignment/README.md](workflow/03_alignment/README.md) for tool logs and command history.

| Metric                           | Value                      |
|----------------------------------|----------------------------|
| Avg raw reads per sample         | `XX million`               |
| Post-trimming retained (%)       | `XX%`                      |
| Alignment/mapping rate (%)       | `XX%`                      |
| Reference genome                 | `GRCh38 / TAIR10 / ...`    |
| Alignment tool                   | `STAR / HISAT2 / Minimap2` |

- ⬜ Are read qualities and mapping rates consistent? Check per-group distribution.


## 3. Gene/Transcript Quantification

See [workflow/04_quantification/README.md](workflow/04_quantification/README.md) for tool logs and command history.

| Metric                           | Value                                   |
|----------------------------------|-----------------------------------------|
| Quantification mode              | alignment-based / alignment-free        |
| Quantification tool              | `featureCounts` / `salmon` / `kallisto` |
| Count threshold used             | `CPM > 1 in ≥ N samples`                |
| Features detected (above threshold) | `X` genes / transcripts              |

- ⬜ Check if gene count distributions vary across groups or outliers exist.


## 4. Differential Expression Analysis

See [workflow/05_dge/README.md](workflow/05_dge/README.md) for tool logs and command history.

| Metric                           | Value       | notes |
|----------------------------------|-------------|-------|
| Tool                             | `DESeq2 / edgeR / limma-voom / ...` | |
| Number of DE genes               |  Z          | adjusted p < 0.05 & |log2FC| > 1 |
| - Upregulated genes              | `X`         |
| - Downregulated genes            | `Y`         |

- ⬜ Is the DEG count biologically plausible? Are negative control comparisons clean?

**Summary Figures:**  

- ⬜ PCA / Clustering  
- ⬜ MA Plot  
- ⬜ Volcano Plot  
- ⬜ Heatmap of top DE genes  

- ⬜ Top DE genes *(table or link to full table in supplementary)*


## 5. Functional Enrichment Analysis

| Enriched categories        | Tool Used             | Notes |
|----------------------------|-----------------------|-------|
| GO: Biological Process     | `clusterProfiler`     |       |
| KEGG / Reactome Pathways   | `gprofiler2 / topGO`  |       |

- ⬜ Are enrichments consistent with known biology? Use correct background sets.

**Visualization**

- ⬜ dotplot, barplot or enrichment map
- ⬜ Number of significant terms: `X` (FDR < 0.05)


## 6. Optional Analyses (if applicable)

### A. Transcript/Isoform Analysis

See [workflow/06_ase/README.md](workflow/06_ase/README.md) for tool logs and command history.

| Metric                    | Value         | Notes |
|---------------------------|---------------|-------|
| Tool(s) used              | `StringTie2, Bambu, satuRn` | |
| Isoforms detected         | `X`           | |
| Differential usage events | `Y`           | |

- ⬜ Is novel transcript detection well-supported by read coverage?


### B. Allele-Specific Expression

| Metric              | Value         | Notes |
|---------------------|---------------|-------|
| Tool(s)             | `MBASED, GATK ASEReadCounter` | |
| ASE loci detected   | `X`           | |

- ⬜ Is there strand or read depth bias? Filter for high-confidence loci.


### C. Fusion Transcript Detection

See [workflow/07_fusion_detection/README.md](workflow/07_fusion_detection/README.md) for tool logs and command history.

| Metric                  | Value      | Notes |
|-------------------------|------------|-------|
| Tool(s) used            | `STAR-Fusion, Arriba` | |
| High-confidence fusions | `X`        | |

- ⬜ Are predicted fusions supported by multiple reads and known breakpoints?


## 7. Summary Tables & Figures

See [07_Supplementary.md](07_Supplementary.md) for supplementary tables.  
Raw figure sources or plotting scripts [workflow/final_report](workflow/final_report) 


# Manuscript Results Paragraph

Draft 1–2 paragraphs summarizing major findings:  
- How many DEGs were found?  
- What pathways or processes are enriched?  
- Were isoform/fusion/cell-type results notable?

Save interpretation for [06_Discussion.md](06_Discussion.md).