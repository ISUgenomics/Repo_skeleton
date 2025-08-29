#### 01_Files &emsp; *List of Raw and Processed Data Files Used in the Project*

[Raw Reads RNA](#raw-reads-rna)  
[Reference Files](#reference-files)  
[Processed Data Outputs](#processed-data-outputs)

---

- **Date created:** [YYYY-MM-DD]
- **Last updated:** [YYYY-MM-DD]
- **HPC Location:** 
  - cluster: @nova
  - project path: `/work/gif4/user/project`

---

- Maintain consistent file naming across tools.
- Store raw data and intermediate files in structured subfolders.
- Always log tool versions and parameters used to generate each file in the respective step’s README.

---


# Raw Reads RNA

**Experiment:** Differential gene expression between wild-type (WT) and atrx-1 mutant to study the role of ATRX histone chaperone.  
**BioProject:** [PRJNA348194](https://www.ncbi.nlm.nih.gov/bioproject/PRJNA348194)  
**Organism:** *Arabidopsis thaliana*  
sequencing mode: **paired-end reads**  


| Sample ID | File Name(s) | Format | Source | Download Method | Notes |
|-----------|--------------|--------|--------|-----------------|-------|
| WT_1 | SRR4420293_1.fastq.gz, SRR4420293_2.fastq.gz | FASTQ (gzipped) | SRA: SRR4420293 | [`wget ftp`](ftp://ftp.sra.ebi.ac.uk/vol1/fastq/SRR442/003/SRR4420293/) | Paired-end |
| WT_2 | SRR4420294_1.fastq.gz, SRR4420294_2.fastq.gz | FASTQ (gzipped) | SRA: SRR4420294 | [`wget ftp`](ftp://ftp.sra.ebi.ac.uk/vol1/fastq/SRR442/004/SRR4420294/) | Paired-end |
| WT_3 | SRR4420295_1.fastq.gz, SRR4420295_2.fastq.gz | FASTQ (gzipped) | SRA: SRR4420295 | [`wget ftp`](ftp://ftp.sra.ebi.ac.uk/vol1/fastq/SRR442/005/SRR4420295/) | Paired-end |
| atrx1_1 | SRR4420296_1.fastq.gz, SRR4420296_2.fastq.gz | FASTQ (gzipped) | SRA: SRR4420296 | [`wget ftp`](ftp://ftp.sra.ebi.ac.uk/vol1/fastq/SRR442/006/SRR4420296/) | Paired-end |
| atrx1_2 | SRR4420297_1.fastq.gz, SRR4420297_2.fastq.gz | FASTQ (gzipped) | SRA: SRR4420297 | [`wget ftp`](ftp://ftp.sra.ebi.ac.uk/vol1/fastq/SRR442/007/SRR4420297/) | Paired-end |
| atrx1_3 | SRR4420298_1.fastq.gz, SRR4420298_2.fastq.gz | FASTQ (gzipped) | SRA: SRR4420298 | [`wget ftp`](ftp://ftp.sra.ebi.ac.uk/vol1/fastq/SRR442/008/SRR4420298/) | Paired-end |


**HPC Location:** 
- path: `/work/gif4/user/project/00_raw_data/`

### IMPORTANT: Confirm File Integrity Check !!!

- status: done / NOT done


---

# Reference Files


| File Type | File Name | Source | Usage in Step | Location |
|-----------|-----------|--------|---------------|----------|
| Genome FASTA | [TAIR10_chr_all.fas.gz](https://www.arabidopsis.org/api/download-files/download?filePath=Genes/TAIR10_genome_release/TAIR10_chromosome_files/TAIR10_chr_all.fas.gz) | [TAIR, 10 release](https://www.arabidopsis.org/download/overview) | Alignment, ASE, Fusion detection | `/work/gif4/user/project/refernce/` |
| Annotation GTF | Arabidopsis_thaliana.TAIR10.56.gtf | Ensembl Plants (release 56) | FeatureCounts, Salmon, HTSeq | `/work/gif4/user/project/03_alignment/ref_assembly/` |
| Transcriptome Index | salmon_index/ | Built using `salmon index` | Quantification (alignment-free) |`/work/gif4/user/project/04_quantification/` |

---

# Processed Data Outputs 

*Update **Filename** and **Location** ! Add more records if needed. &emsp; (to be filled during analysis)*

| File Type | Description | Format | Filename(s) | Location | Analysis Step |
|-----------|-------------|--------|-------------|----------|---------------|
| Aligned Reads        | BAM files for each replicate | `.bam`, `.bai` | `sampleX.bam`, `sampleX.bam.bai` | `/work/gif4/user/project/03_alignment/`          | Read alignment to reference genome            |
| Count Matrix         | Raw gene-level counts        | `.txt`, `.tsv` | `counts_matrix.txt`              | `/work/gif4/user/project/04_quantification/`     | Gene/transcript quantification                |
| TPM Quantification   | Transcript-level TPM values  | `.sf`          | `quant.sf`                       | `/work/gif4/user/project/04_quantification/`     | Gene/transcript quantification                |
| Normalized Counts    | DESeq2-normalized counts     | `.rds`, `.csv` | `norm_counts.rds`, `norm_counts.csv` | `/work/gif4/user/project/05_dge/1_analysis/` | Differential gene expression analysis         |
| DEG Results          | Fold change, p-values, padj  | `.csv`         | `DEG_results.csv`                | `/work/gif4/user/project/05_dge/1_analysis/`     | Differential gene expression analysis         |
| DEG Plots            | PCA, volcano, heatmaps       | `.png`, `.pdf` | `pca_plot.png`, `volcano_plot.pdf`| `/work/gif4/user/project/05_dge/3_plots/`       | Visualization of differential expression data |
| Enrichment Analysis  | GO, KEGG, GSEA output        | `.xlsx`, `.tsv`| `go_enrichment.xlsx`, `kegg.tsv` | `/work/gif4/user/project/05_dge/2_downstream/`   | Functional and enrichment analysis            |

---

## Optional Files

*Update **Filename** and **Location** ! Add or remove records if needed. &emsp; (to be filled during analysis)*

| File Type | Description | Format | Filename(s) | Location | Analysis Step |
|-----------|-------------|--------|-------------|----------|---------------|
| ASE Input VCF       | Variant calls for ASE analysis | `.vcf.gz` | `cohort_phased.vcf.gz`       | `/work/gif4/user/project/06_ase/0-config/`                | Allele-specific expression analysis |
| Fusion Predictions  | STAR-Fusion or Arriba outputs  | `.tsv`    | `starfusion_predictions.tsv` | `/work/gif4/user/project/07_fusion_detection/1_analysis/` | Fusion transcript detection         |
