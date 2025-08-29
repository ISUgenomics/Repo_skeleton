#### 03_Methods &emsp; *This document records the experimental and computational methods*

[Experimental Methods](#experimental-methods)  
[Computational Methods & Tools](#computational-methods)  
[Manuscript Methods Paragraph](#manuscript-methods-paragraph)  

---

- **Date created:** [YYYY-MM-DD]
- **Last updated:** [YYYY-MM-DD]

---

- Remove unused steps from this report (all options are listed in this template).
- Document all tools used, including exact versions and parameters.
- For each analysis step, list key decisions and tool-specific settings.
- Review the [Manuscript Methods Paragraph](#manuscript-methods-paragraph) that can be directly used in your publication.

---

This document records the **experimental** and **computational methods** used in this RNA-seq analysis.  
Each section includes tools used, rationale, parameter choices and commands for reproducibility.

## Experimental Methods

This table summarizes key experimental details for your bulk RNA-seq project. It will help standardize documentation and simplify the writing of your manuscript methods section.

*Please update the "Description" column with your specific project metadata. Leave empty if no data for the specific attribute.*

| Step                    | Description                                  |
|-------------------------|----------------------------------------------|
| Organism                | *Arabidopsis thaliana*                       |
| Tissue/Material         | Whole seedling                               |
| Genotypes               | WT, atrx-1 mutant                            |
| RNA Isolation Method    | Trizol reagent                               |
| RNA Enrichment          | Plant RiboMinus Kit (total RNA depletion)    |
| Sequencing Platform     | Illumina HiSeq 2500                          |
| Read Type               | short-read, **paired-end**, 2 × 100 bp       |
| Replicates              | **3 biological replicates per group**        |

## Computational Methods

Copy the [step selection checklist](/workflow/README#step-selection-checklist) from the `workflow/README.md` and **remove any steps or tools not used in your project**. Keep only the analysis stages and software tools that were actually executed during your workflow.


| check | step - full docs | tools | version | description | notes |
|-------|------------------|-------|---------|-------------|-------|
| [x] | [**00_raw_data/**](workflow/00_raw_data/) | `wget`, `sratoolkit`  |x.x| download and verify raw FASTQ files |  
| [x] | [**01_read_qc/**](workflow/1_read_qc/) | `FastQC`, `MultiQC`      |x.x| raw read quality control | 
| [x] | [**02_trimming/**](workflow/2_trimming/) | `fastp`, `Trim Galore`, `cutadapt`, `Trimmomatic` |x.x| red trimming & filtering |  
| [x] | [**03_alignment/**](workflow/03_alignment/) | `STAR`, `HISAT2`, `minimap2`, `samtools` |x.x| align reads to reference | 
| [x] | [**04_quantification/**](workflow/4_quantification/) |  || expression quantification at transcript/gene level |   
| [x] | **A. alignment-based/** | `featureCounts`, `htseq-count` |x.x| requires aligned reads (BAMs from 03_alignment) |  
| [ ] | **B. alignment-free/**  | `Salmon`, `kallisto`        |x.x| quasi-mapping to transcriptome; skips alignment step |   
| [x] | [**05_dge/**](workflow/5_dge/) | `DESeq2`, `edgeR`, `limma-voom`, `tximport`, `biomaRt` |x.x| differential gene expression |
| [ ] | [**06_ase/**](workflow/06_ase/) | `GATK ASEReadCounter`, `phASER`, `MBASED` |x.x| allele-specific expression |  
| [ ] | [**07_fusion_detection/**](workflow/07_fusion_detection/) | `STAR-Fusion`, `Arriba`, `FusionCatcher` |x.x| fusion transcript |  
| [x] | [**final_report/**](workflow/final_report/) | `RMarkdown`, `ggplot2`, `pheatmap`, `EnhancedVolcano`, `clusterProfiler` |x.x| workflow summary, figures, tables for manuscript |   



## Manuscript Methods Paragraph

*Please replace bracketed text and options with actual run metadata, tool versions and parameter values.*

Total RNA was extracted from [organism: Arabidopsis thaliana] [wild-type (WT)] and [atrx-1 mutant] [tissue: seedlings] using [Trizol reagent], following the manufacturer's protocol. To enrich for messenger RNA, [ribosomal RNA] was depleted using the [Plant RiboMinus kit]. RNA integrity was assessed using a [Bioanalyzer or TapeStation], and library preparation was performed using a [paired-end stranded mRNA-seq protocol]. Sequencing was carried out on an [Illumina HiSeq 2500] platform, producing [2×100 bp paired-end] short reads.

Raw sequencing data (FASTQ files) were retrieved from [NCBI SRA, BioProject PRJNA348194] using the wget command-line tool, and file integrity was confirmed via MD5 checksum comparison. Pre- and post-trimming quality control was performed using [FastQC (vX.X)] and summarized with [MultiQC (vX.X)]. Adapter sequences and low-quality bases were removed using [fastp (vX.X)] with the following key parameters: [`--detect_adapter_for_pe`, `--cut_front`, `--cut_tail`, `--qualified_quality_phred 15`, and `--length_required 36`].

> (option 1)
For gene expression quantification, the alignment-based strategy was employed. Trimmed reads were aligned to the [Arabidopsis thaliana TAIR10 reference genome] using [**option 1:** STAR (vX.X) in two-pass mode with default parameters; **option 2:** HISAT2 (vX.X) with the `--dta` option to preserve transcript structure]. The resulting alignments were sorted and indexed using [samtools (vX.X)]. Gene-level quantification was performed using [featureCounts (vX.X)], guided by the corresponding gene annotation file in GTF format.

> (option 2)
An alignment-free approach was used for transcript quantification. Trimmed reads were processed using [Salmon (vX.X)] in quasi-mapping mode against a transcriptome index built from the [TAIR10 or EnsemblPlants] transcriptome. This method generated transcript-level abundance estimates (TPM) as well as effective read counts.

Differential gene expression analysis was conducted in R (vX.X) using the [**option 1:** DESeq2 (vX.X) package; **option 2:** edgeR (vX.X) package; **option 3:** limma (vX.X) with the voom transformation]. Raw gene counts were filtered to remove lowly expressed genes and normalized using [option 1: the median-of-ratios method (DESeq2); option 2: TMM normalization (edgeR and limma)]. A [design formula: ~ genotype] was used to model expression differences between wild-type and atrx-1 samples.  
> *(option: DESeq2)* Dispersion estimates were obtained using `estimateDispersions`, and the Wald test was applied.  
> *(option: edgeR)* A negative binomial model was fitted, and the likelihood ratio test was used to assess differential expression.  
> *(option: limma-voom)* The voom function transformed count data into log2 counts per million with associated precision weights, followed by linear modeling and empirical Bayes moderation of variance estimates.  

P-values were corrected for multiple testing using the Benjamini-Hochberg procedure. Genes were considered significantly differentially expressed if they satisfied the thresholds of adjusted p-value < 0.05 and |log₂ fold change| > 1.

Downstream einrichment analysis of the differentially expressed genes (DEGs) was performed using [clusterProfiler (vX.X)] for Gene Ontology (GO) terms, and [gprofiler2 (vX.X)] or [topGO (vX.X)] for pathway analysis including KEGG and Reactome annotations. Visualization of results, including PCA plots, MA plots, volcano plots, and clustered heatmaps, was performed using [ggplot2 (vX.X)], [EnhancedVolcano (vX.X)], and [pheatmap (vX.X)].

*(optional, if ASE applicable)*
>To further investigate allele-specific transcriptional activity, allele-specific expression (ASE) analysis was performed. Aligned BAM files and matched VCF variant files were analyzed using [GATK ASEReadCounter (vX.X)] to extract allele counts, and [phASER (vX.X)] was used to phase variants and model ASE patterns. ASE significance was further assessed using [MBASED (vX.X)] with default binomial modeling parameters.

*(optional, if Fusion detection applicable)*
> In addition to [gene- and allele-level analyses], fusion transcript detection was conducted to uncover potential gene fusion events that may contribute to altered transcriptional profiles in the mutant condition. Aligned BAM files were analyzed using [**option 1:** STAR-Fusion (vX.X) with default parameters and post-filtering enabled **option 2:** Arriba (vX.X) configured for strand-specific, paired-end input]. 
Predicted fusion events were filtered based on supporting read evidence (split and discordant reads), junction confidence, and read-through artifact exclusion. Annotations were enriched using domain-aware references such as [FusionAnnotator, COSMIC, and OncoKB], allowing classification of fusion candidates by functional impact and known oncogenic potential. To support interpretation, selected high-confidence fusions were visualized with [IGV] or reconstructed via [FusionInspector] to validate junction structure and supporting read architecture.
