#### 02_Metadata &emsp; *This file documents the metadata associated with all RNA-seq samples*

[Experimental Design](#experimental-design)  
[Metadata Table](#metadata-table)  
[Sample Grouping](#sample-grouping)

---

- **Date created:** [YYYY-MM-DD]
- **Last updated:** [YYYY-MM-DD]

---

- Maintain a clear and consistent format for sample names and conditions.
- Ensure sample IDs match exactly across metadata, FASTQ files, and downstream analyses.
- Include experimental variables (e.g., genotype, treatment, timepoint) explicitly for modeling.
- Record clinical or biological attributes if available (e.g., age, tissue type, developmental stage).
- Save both raw metadata (as received) and curated/cleaned versions used in analysis.

---

## Experimental Design

Provide a brief description of the experimental design:

> This study compares gene expression in wild-type (*WT*) and **atrx-1 mutant** *Arabidopsis thaliana* seedlings. RNA was extracted from whole tissue in three biological replicates per group. RNA-seq was carried out in Illumina Hiseq 2500. The sequencing reads were generated as paired-end data, hence we have 2 files per replicate.  The aim is to investigate the transcriptional consequences of ATRX loss-of-function.

### Experimental Notes

- RNA was extracted using Trizol
- rRNA was depleted using Plant RiboMinus kit
- Libraries were prepared for total RNA sequencing
- Sequencing performed on **Illumina HiSeq 2500**
  - sequencing mode: **paired-end**



## Metadata Table

- **BioProject:** [PRJNA348194](https://www.ncbi.nlm.nih.gov/bioproject/PRJNA348194)  
- **Organism:** *Arabidopsis thaliana*  
- **HPC Location:** 
  - cluster: @nova
  - metadata path: `/work/gif4/user/project/00_raw_data/sample_sheet.tsv`

Include all relevant variables (sample ID, genotype, replicate, treatment, batch, etc.).  
*Update or extend columns as needed (e.g., for treatment duration, tissue type, sex, age, batch ID, etc.)*

| Sample ID | Genotype | Condition | Replicate | Run Accession | Library Type | Layout     | Notes |
|-----------|----------|-----------|-----------|---------------|--------------|------------|-------|
| `WT_R1`   | WT       | Control   | 1         | SRR4420293    | total RNA    | Paired-end |       |
| `WT_R2`   | WT       | Control   | 2         | SRR4420294    | total RNA    | Paired-end |       |
| `WT_R3`   | WT       | Control   | 3         | SRR4420295    | total RNA    | Paired-end |       |
| `m_R1`    | atrx-1   | Mutant    | 1         | SRR4420296    | total RNA    | Paired-end |       |
| `m_R2`    | atrx-1   | Mutant    | 2         | SRR4420297    | total RNA    | Paired-end |       |
| `m_R3`    | atrx-1   | Mutant    | 3         | SRR4420298    | total RNA    | Paired-end |       |

**NOTE:** Keep this table synchronized with your `count-matrix` and DESeq2 `sample-sheet`.

### Sample Grouping

Describe how samples are grouped for analysis:

- **Group A:** WT (Control) - `WT_R1`, `WT_R2`, `WT_R3`  
- **Group B:** atrx-1 mutant - `m_R1`, `m_R2`, `m_R3`  

These groups will be used to define contrasts for differential expression analysis.



