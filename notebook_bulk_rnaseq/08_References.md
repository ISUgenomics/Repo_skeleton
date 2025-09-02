#### 08_References &emsp; *This document compiles all experimental and computational literature references*

[0. Best-practice Overviews & Standards](#0-best-practice-overviews--standards)  
[1. Experimental Protocols, Advances in Sequencing Technologies](#1-experimental-protocols-advances-in-sequencing-technologies)  
[2. Reference Data and Annotation Sources](#2-reference-data-and-annotation)  
[3. Computational Tools](#3-computational-tools)
  - [Quality Control and Trimming/Filtering](#quality-control-and-trimmingfiltering)
  - [Alignment and Quantification](#alignment-and-quantification)
  - [Differential Expression Analysis](#differential-expression-analysis)
  - [ASE / Fusion Detection (optional)](#ase--fusion-detection-optional)
  - [Other Applications (optional)](#other-applications-optional)

[4. Workflow Engines, Automation & Reproducibility](#4-workflow-engines-automation--reproducibility)

[**Manuscript Literature References**](#manuscript-literature-references) *(edit your references here)*

---

- **Date created:** [YYYY-MM-DD]  
- **Last updated:** [YYYY-MM-DD]  

---

- List all tools, resources, databases and protocols used throughout the pipeline.
- Group references by analysis stage or data type to ease manuscript preparation.
- Include DOIs, PubMed IDs or links where applicable.

---

This file provides an organized overview of relevant literature references across key categories of RNA-seq analysis. Browse the tables below to explore tools and methods, with direct links to the corresponding publications for deeper reading. **The final section includes a compiled list of all citations - ready to prune, extend and use during manuscript preparation.**

## 0. Best-practice Overviews & Standards

| Tool / Topic                                    | Citation                                               | DOI / Link |
|-------------------------------------------------|--------------------------------------------------------|------------|
| RNA-seq best practices (overview)               | Conesa et al., 2016, Genome Biology, 17(1)             | [10.1186/s13059-016-0881-8](https://doi.org/10.1186/s13059-016-0881-8) |
| RNA-seq guide for nonexperts                    | Lee G-Y et al., 2024, Molecules and Cells, 47(5)       | [10.1016/j.mocell.2024.100060](https://doi.org/10.1016/j.mocell.2024.100060) |
| RNA-seq workflow optimization benchmark         | Jiang et al., 2024, BMC Genomics                       | [10.1186/s12864-024-10414-y](https://doi.org/10.1186/s12864-024-10414-y) |
| Long-read transcriptomics (review)              | Monzó et al., 2025, Nat Rev Genet                      | [10.1038/s41576-025-00828-z](https://doi.org/10.1038/s41576-025-00828-z) |


## 1. Experimental Protocols, advances in sequencing technologies 

Include references for RNA extraction method (e.g., Trizol), library preparation kit/protocol, sequencing platform and general RNA-seq protocols.

| Tool / Method                | Citation                                       | DOI / Link |
|------------------------------|------------------------------------------------|------------|
| Trizol RNA extraction        | Chomczynski & Sacchi, 2006, Nat Protoc         | [10.1038/nprot.2006.83](https://doi.org/10.1038/nprot.2006.83) |
| Bulk RNA-seq standard        | Wang et al., 2009, Nat Rev Genet               | [10.1038/nrg2484](https://doi.org/10.1038/nrg2484) |
| all RNA-seq technology overview | Stark et al., 2019, Nature Reviews Genetics | [10.1038/s41576-019-0150-2](https://doi.org/10.1038/s41576-019-0150-2) |

| **Short-Read Sequencing**                            | Citation                                                            | DOI / Link |
|------------------------------------------------------|---------------------------------------------------------------------|------------|
| Illumina NextSeq vs MGI DNBSEQ (bulk)                | Póliska et al., 2024, Front Genet, 14:1275383                       | [10.3389/fgene.2023.1275383](https://doi.org/10.3389/fgene.2023.1275383) |
| Early barcoding for cost-efficient bulk RNA-seq      | Janjic et al., 2022, Genome Biology, 23:88                          | [10.1186/s13059-022-02660-8](https://doi.org/10.1186/s13059-022-02660-8) |

| **Long-Read Sequencing**                                       | Citation                                                           | DOI / Link |
|----------------------------------------------------------------|--------------------------------------------------------------------|------------|
| Long-read RNA-seq benchmark (LRGASP: PacBio & ONT)             | Pardo-Palacios et al., 2024, Nat Methods, 21:1349–1363             | [10.1038/s41592-024-02298-3](https://doi.org/10.1038/s41592-024-02298-3) |
| Nanopore sequencing review                                     | Wang et al., 2021, Nat Biotechnol, 39                              | [10.1038/s41587-021-01108-x](https://doi.org/10.1038/s41587-021-01108-x) |
| SG-NEx benchmark (Illumina, ONT, PacBio)                       | Chen et al., 2025, Nat Methods, 22:801–812                         | [10.1038/s41592-025-02623-4](https://doi.org/10.1038/s41592-025-02623-4) |
| Direct RNA-seq in viral transcriptomes                         | Depledge et al., 2019, Nat Commun, 10                              | [10.1038/s41467-019-08734-9](https://doi.org/10.1038/s41467-019-08734-9) |


## 2. Reference Data and Annotation

Include references for: genome assembly, gene annotation files (e.g., GTF from EnsemblPlants or Araport11), reference index, SNP/VCF files (for ASE or phasing).

| Resource                 | Citation                                        | DOI / Link |
|--------------------------|-------------------------------------------------|------------|
| genome assembly (e.g., Arabidopsis) | The Arabidopsis Information Resource (TAIR)     | [arabidopsis.org](https://www.arabidopsis.org/) |
| annotation (e.g., Araport11)        | Cheng et al., 2017, Nucleic Acids Res           | [10.1093/nar/gkw1008](https://doi.org/10.1093/nar/gkw1008) |
| EnsemblPlants            | EnsemblPlants Reference Genome Release          | [plants.ensembl.org](https://plants.ensembl.org/) |
| 1001 Genomes Project     | 1001 Genomes Consortium                         | [1001genomes.org](https://1001genomes.org/) |


## 3. Computational Tools

### Quality Control and Trimming/Filtering

| Tool           | Citation                                      | DOI / Link |
|----------------|-----------------------------------------------|------------|
| FastQC         | Andrews S, 2010, Babraham Bioinformatics      | [www.bioinformatics.babraham.ac.uk/projects/fastqc](https://www.bioinformatics.babraham.ac.uk/projects/fastqc/) |
| MultiQC        | Ewels et al., 2016, Bioinformatics            | [10.1093/bioinformatics/btw354](https://doi.org/10.1093/bioinformatics/btw354) |
| fastp          | Chen et al., 2018, Bioinformatics             | [10.1093/bioinformatics/bty560](https://doi.org/10.1093/bioinformatics/bty560) |
| Trimmomatic    | Bolger et al., 2014, Bioinformatics           | [10.1093/bioinformatics/btu170](https://doi.org/10.1093/bioinformatics/btu170) |
| Cutadapt       | Martin et al., 2011, EMBnet.journal           | [10.14806/ej.17.1.200](https://doi.org/10.14806/ej.17.1.200) |

### Alignment and Quantification

* **splice-aware alignment** 

| Task                   | Tool           | Citation                                      | DOI / Link |
|------------------------|----------------|-----------------------------------------------|------------|
| transcriptome assembly | StringTie2     | Kovaka et al., 2019, *Genome Biology*, 20(1), 278                                              | [10.1186/s13059-019-1910-1](https://doi.org/10.1186/s13059-019-1910-1) |
| alignment              | STAR           | Dobin et al., 2013, Bioinformatics            | [10.1093/bioinformatics/bts635](https://doi.org/10.1093/bioinformatics/bts635) |
| alignment              | HISAT2         | Kim et al., 2019, Nature Biotechnology        | [10.1038/s41587-019-0201-4](https://doi.org/10.1038/s41587-019-0201-4) |
| alignment              | Minimap2       | Li, 2018, Bioinformatics                      | [10.1093/bioinformatics/bty191](https://doi.org/10.1093/bioinformatics/bty191) |
| quantification         | featureCounts  | Liao et al., 2014, Bioinformatics             | [10.1093/bioinformatics/btt656](https://doi.org/10.1093/bioinformatics/btt656) |


* **quasi-mapping** (alignment-free)

| Tool           | Citation                                      | DOI / Link |
|----------------|-----------------------------------------------|------------|
| Salmon         | Patro et al., 2017, Nat Methods               | [10.1038/nmeth.4197](https://doi.org/10.1038/nmeth.4197) |
| Kallisto       | Bray et al., 2016, Nature Biotechnology       | [10.1038/nbt.3519](https://doi.org/10.1038/nbt.3519)     |

### Differential Expression Analysis

| Tool            | Citation                                     | DOI / Link |
|-----------------|----------------------------------------------|------------|
| DESeq2          | Love et al., 2014, Genome Biol               | [10.1186/s13059-014-0550-8](https://doi.org/10.1186/s13059-014-0550-8) |
| DESeq2 + apeglm | Zhu et al., 2019, Bioinformatics             | [10.1093/bioinformatics/bty895](https://doi.org/10.1093/bioinformatics/bty895) |
| edgeR           | Robinson et al., 2010, Bioinformatics        | [10.1093/bioinformatics/btp616](https://doi.org/10.1093/bioinformatics/btp616) |
| limma-voom      | Law et al., 2014, Trends Genet               | [10.1186/gb-2014-15-2-r29](https://doi.org/10.1186/gb-2014-15-2-r29) |
| dream (limma)   | Hoffman & Roussos, 2021, Bioinformatics      | [10.1093/bioinformatics/btaa687](https://doi.org/10.1093/bioinformatics/btaa687) |
| tximport        | Soneson et al., 2016, F1000Research          | [10.12688/f1000research.7563.2](https://doi.org/10.12688/f1000research.7563.2) |

### Functional/Enrichment Analysis

| Tool / Method      | Citation                                  | DOI / Link |
|--------------------|-------------------------------------------|------------|
| clusterProfiler    | Yu et al., 2012, OMICS                    | [10.1089/omi.2011.0118](https://doi.org/10.1089/omi.2011.0118) |
| gprofiler2         | Kolberg et al., 2020, F1000Res            | [10.12688/f1000research.24956.2](https://doi.org/10.12688/f1000research.24956.2) |
| topGO              | Alexa et al., 2006, Springer              | [10.1007/0‑387‑29362‑0_27](https://link.springer.com/book/10.1007/0-387-29362-0) |

| Visualization and Reporting     | Citation                     | DOI / Link |
|---------------------------------|------------------------------|------------|
| EnhancedVolcano    | Blighe et al., Bioconductor               | [github.com/kevinblighe/EnhancedVolcano](https://github.com/kevinblighe/EnhancedVolcano) |
| pheatmap           | Kolde, Bioconductor                       | [CRAN](https://cran.r-project.org/package=pheatmap) |
| ggplot2            | Wickham, 2016, Springer                   | [10.1007/978-3-319-24277-4](https://doi.org/10.1007/978-3-319-24277-4) |


### ASE / Fusion Detection (optional)

| Topic              | Tool / Method  | Citation                                    | DOI / Link |
|--------------------|----------------|---------------------------------------------|------------|
| Allelic expression | GATK ASE tools | DePristo et al., 2011, Nature Genetics      | [10.1038/ng.806](https://doi.org/10.1038/ng.806) |
| Allelic expression | phASER         | Castel et al., 2016, Nature Communications  | [10.1038/ncomms12817](https://doi.org/10.1038/ncomms12817) |
| Allelic expression | MBASED         | Mayba et al., 2014, Nature Methods          | [10.1186/s13059-014-0405-3](https://doi.org/10.1186/s13059-014-0405-3) |
| Fusion detection   | STAR-Fusion    | Haas et al., 2019, Genome Biology           | [10.1186/s13059-019-1842-9](https://doi.org/10.1186/s13059-019-1842-9) |
| Fusion detection   | Arriba         | Uhrig et al., 2021, Genome Research         | [10.1101/gr.257246.119](https://doi.org/10.1101/gr.257246.119) |


### Other Applications (optional)

| Topic            | Tool / Method                 | Citation                                                           | DOI / Link |
|------------------|-------------------------------|--------------------------------------------------------------------|------------|
| Isoform quantification         | Bambu           | Chen et al., 2023, Nature Methods, 20(8), 1187–1195                | [10.1038/s41592-023-01908-w](https://doi.org/10.1038/s41592-023-01908-w) |
| Differential transcript usage  | satuRn          | Gilis et al., 2021, F1000Research, 10, 374                         | [10.12688/f1000research.51749.2](https://doi.org/10.12688/f1000research.51749.2) |
| Co-expression networks         | WGCNA           | Langfelder et al., 2008, BMC Bioinformatics, 9, article 559        | [10.1186/1471-2105-9-559](https://doi.org/10.1186/1471-2105-9-559) |
| eQTL mapping                   | eQTL Catalogue  | Kerimov et al., 2023, PLOS Genetics, 19(9), e1010932               | [10.1371/journal.pgen.1010932](https://doi.org/10.1371/journal.pgen.1010932) |
| Cell-type deconvolution        | CIBERSORTx      | Newman et al., 2019, Nature Biotechnology, 37(7), 773–782          | [10.1038/s41587-019-0114-2](https://doi.org/10.1038/s41587-019-0114-2) |
| Method benchmarking            | DREAM Deconvolution Challenge  | White et al., 2024, Nature Communications, 15, 7362 | [10.1038/s41467-024-50618-0](https://doi.org/10.1038/s41467-024-50618-0) |
| RNA editing annotation         | REDIportal      | D’Addabbo et al., 2025, Nucleic Acids Research, 53(D1), D233–D242  | [10.1093/nar/gkae1083](https://doi.org/10.1093/nar/gkae1083) |


## 4. Workflow Engines, Automation & Reproducibility

| Tool / Workflow      | Citation                                                              | DOI / Link |
|----------------------|-----------------------------------------------------------------------|------------|
| systemPipeR          | Backman et al., 2016, BMC Bioinformatics, 17(1)                       | [10.1186/s12859-016-1241-0](https://doi.org/10.1186/s12859-016-1241-0) |
| nf-core/rnaseq       | Perelo et al., 2024, NAR Genomics and Bioinformatics, 6(1), lqae020   | [10.1093/nargab/lqae020](https://doi.org/10.1093/nargab/lqae020) |
| ARMOR                | Orjuela et al., 2019, G3: Genes,Genomes,Genetics, 9(7), 2089–2096     | [10.1534/g3.119.400185](https://doi.org/10.1534/g3.119.400185) |
| RASflow              | Zhang et al., 2020, BMC Bioinformatics, 21, Article 110               | [10.1186/s12859-020-3433-x](https://doi.org/10.1186/s12859-020-3433-x) |
| VIPER                | Cornwell et al., 2018, BMC Bioinformatics, 19(1), 135                 | [10.1186/s12859-018-2139-9](https://doi.org/10.1186/s12859-018-2139-9) |
| SPEAQeasy            | Eagles et al., 2021, BMC Bioinformatics, 22, Article 224              | [10.1186/s12859-021-04142-3](https://doi.org/10.1186/s12859-021-04142-3) |



# Manuscript Literature References

*Please carefully review the categorized citations listed in this section. Remove any references that are not relevant to your manuscript. The remaining entries can be directly referenced in your text or copy-pasted into bibliography as needed. Feel free to extend the compiled list with additional literature references you used during analysis or manuscript preparation.*

```markdown
# Best-practice Overviews & Standards
1. Conesa A, Madrigal P, Tarazona S, et al. A survey of best practices for RNA-seq data analysis. Genome Biol. 2016;17(1):13. doi:10.1186/s13059-016-0881-8.
2. Lee G-Y, Kim K, Lee S, et al. Brief guide to RNA sequencing analysis for nonexperts in bioinformatics. Molecules and Cells. 2024;47(5):100060. doi:10.1016/j.molcel.2024.100060.
3. Zhou Y, Xia Z, Li S, et al. A comprehensive workflow for optimizing RNA-seq data analysis. BMC Genomics. 2024;25:631. doi:10.1186/s12864-024-10248-4.
4. Monzó P, Steijger T, Reuter JA, et al. Transcriptomics in the era of long-read sequencing. Nat Rev Genet. 2025. doi:10.1038/s41576-025-00790-6.
```

```markdown
# Experimental Protocols, advances in sequencing technologies 
1. Chomczynski P, Sacchi N. The single-step method of RNA isolation by acid guanidinium thiocyanate-phenol-chloroform extraction: twenty-something years on. Nat Protoc. 2006;1(2):581–585. doi:10.1038/nprot.2006.83.
2. Wang Z, Gerstein M, Snyder M. RNA-Seq: a revolutionary tool for transcriptomics. Nat Rev Genet. 2009;10(1):57–63. doi:10.1038/nrg2484.
3. Stark R, Grzelak M, Hadfield J. RNA sequencing: the teenage years. Nature Reviews Genetics. 2019;20:631–656. doi:10.1038/s41576-019-0150-2.

## Short-Read Sequencing 
1. Póliska S, Vancsik T, Szabo V, et al. Comparative transcriptomic analysis of Illumina and MGI platforms using embryonic stem cells. Front Genet. 2024;14:1275383. doi:10.3389/fgene.2023.1275383.
2. Janjic A, Collado-Torres L, Luo C, et al. Prime-seq, efficient and powerful bulk RNA sequencing. Genome Biol. 2022;23:88. doi:10.1186/s13059-022-02652-5.

## Long-Read Sequencing
1. Pardo-Palacios F, Piskol R, Garcia A, et al. Systematic assessment of long-read RNA-seq methods. Nat Methods. 2024;21:1349–1363. doi:10.1038/s41592-024-02180-y.
2. Wang Y, Yang Q, Wang Z. Nanopore sequencing: technology, bioinformatics and applications. Nat Biotechnol. 2021;39:1348–1355. doi:10.1038/s41587-021-01108-x.
3. Chen Z, Tan W, Lau E, et al. A systematic benchmark of Nanopore long-read RNA sequencing. Nat Methods. 2025;22:801–812. doi:10.1038/s41592-024-02162-0.
4. Depledge DP, Srinivas KP, Sadaoka T, et al. Direct RNA sequencing redefines the transcriptional complexity of a viral pathogen. Nat Commun. 2019;10:754. doi:10.1038/s41467-019-08734-9.
```


```markdown
# Tools: Quality Control and Trimming/Filtering
1. Ewels P, Magnusson M, Lundin S, Käller M. MultiQC: summarize analysis results for multiple tools and samples in a single report. Bioinformatics. 2016;32(19):3047–3048. doi:10.1093/bioinformatics/btw354.
2. Chen S, Zhou Y, Chen Y, Gu J. fastp: an ultra-fast all-in-one FASTQ preprocessor. Bioinformatics. 2018;34(17):i884–i890. doi:10.1093/bioinformatics/bty560.
3. Bolger AM, Lohse M, Usadel B. Trimmomatic: a flexible trimmer for Illumina sequence data. Bioinformatics. 2014;30(15):2114–2120. doi:10.1093/bioinformatics/btu170.
4. Martin M. Cutadapt removes adapter sequences from high-throughput sequencing reads. EMBnet.journal. 2011;17(1):10–12. doi:10.14806/ej.17.1.200.
```

```markdown
# Tools: Alignment/Mapping and Quantification
0. Kovaka S, Zimin AV, Pertea GM, et al. Transcriptome assembly from long-read RNA-seq alignments with StringTie2. Genome Biol. 2019;20(1):278. doi:10.1186/s13059-019-1910-1.
1. Dobin A, Davis CA, Schlesinger F, et al. STAR: ultrafast universal RNA-seq aligner. Bioinformatics. 2013;29(1):15–21. doi:10.1093/bioinformatics/bts635.
2. Kaminow B, Yunusov D, Dobin A. STARsolo: accurate, fast and versatile mapping/quantification of single-cell and single-nucleus RNA-seq data. bioRxiv. 2021. doi:10.1101/2021.05.05.442755.
3. Kim D, Langmead B, Salzberg SL. HISAT: a fast spliced aligner with low memory requirements. Nat Methods. 2015;12(4):357–360. doi:10.1038/nmeth.3317.
4. Kim D, Paggi JM, Park C, Bennett C, Salzberg SL. Graph-based genome alignment and genotyping with HISAT2 and HISAT-genotype. Nat Biotechnol. 2019;37(8):907–915. doi:10.1038/s41587-019-0201-4.
5. Li H. Minimap2: pairwise alignment for nucleotide sequences. Bioinformatics. 2018;34(18):3094–3100. doi:10.1093/bioinformatics/bty191.
6. Zhang W, Yu C, Lin J, et al. Rapid and accurate alignment of nucleotide conversion sequencing reads with HISAT-3N. Genome Res. 2021;31(7):1290–1295. doi:10.1101/gr.275193.120.
7. Li H. New strategies to improve minimap2 alignment accuracy. Bioinformatics. 2021;37(23):4572–4574. doi:10.1093/bioinformatics/btab705.
8. Liao Y, Smyth GK, Shi W. featureCounts: an efficient general purpose program for assigning sequence reads to genomic features. Bioinformatics. 2014;30(7):923–930. doi:10.1093/bioinformatics/btt656.
9. Patro R, Duggal G, Love MI, Irizarry RA, Kingsford C. Salmon provides fast and bias-aware quantification of transcript expression. Nat Methods. 2017;14(4):417–419. doi:10.1038/nmeth.4197.
10. Bray NL, Pimentel H, Melsted P, Pachter L. Near-optimal probabilistic RNA-seq quantification. Nat Biotechnol. 2016;34(5):525–527. doi:10.1038/nbt.3519.
```

```markdown
# Downstream: Differential Expression Analysis
1. Love MI, Huber W, Anders S. Moderated estimation of fold change and dispersion for RNA-seq data with DESeq2. Genome Biol. 2014;15(12):550. doi:10.1186/s13059-014-0550-8.
2. Zhu A, Ibrahim JG, Love MI. Heavy-tailed prior distributions for sequence count data: removing noise while preserving large differences. Bioinformatics. 2019;35(12):2084–2092. doi:10.1093/bioinformatics/bty895.
3. Robinson MD, McCarthy DJ, Smyth GK. edgeR: a Bioconductor package for differential expression analysis of digital gene expression data. Bioinformatics. 2010;26(1):139–140. doi:10.1093/bioinformatics/btp616.
4. Chen Y, Lun ATL, McCarthy DJ, Ritchie ME, Smyth GK. edgeR v4: powerful differential analysis of sequencing data. Nucleic Acids Res. 2025;53(2):gkaf018. doi:10.1093/nar/gkaf018.
5. Law CW, Chen Y, Shi W, Smyth GK. voom: precision weights unlock linear model analysis tools for RNA-seq read counts. Genome Biol. 2014;15(2):R29. doi:10.1186/gb-2014-15-2-r29.
6. Hoffman GE, Roussos P. Dream: powerful differential expression analysis for repeated-measures designs. Bioinformatics. 2021;37(2):192–201. doi:10.1093/bioinformatics/btaa687.
7. Soneson C, Love MI, Robinson MD. Differential analyses for RNA-seq: transcript-level estimates improve gene-level inferences. F1000Research. 2016;4:1521. doi:10.12688/f1000research.7563.2.
```

```markdown
# Downstream: Functional/Enrichment Analysis
1. Yu G, Wang LG, Han Y, He QY. clusterProfiler: an R package for comparing biological themes among gene clusters. OMICS. 2012;16(5):284–287. doi:10.1089/omi.2011.0118.
2. Kolberg L, Raudvere U, Kuzmin I, Vilo J, Peterson H. gprofiler2: an R package for gene list functional enrichment analysis and namespace conversion toolset. Nucleic Acids Res. 2020;48(W1):W191–W198. doi:10.1093/nar/gkaa226.
3. Alexa A, Rahnenführer J. Gene set enrichment analysis with topGO. In: Gentleman R, Carey VJ, Huber W, Irizarry RA, Dudoit S, editors. Bioinformatics and Computational Biology Solutions Using R and Bioconductor. New York: Springer; 2006. p. 493–509. doi:10.1007/0‑387‑29362‑0_27.
4. Wickham H. ggplot2: Elegant Graphics for Data Analysis. Springer; 2016. xxvi+260 pp. ISBN: 978-3-319-24277-4. doi:10.1007/978-3-319-24277-4
```

```markdown
# Downstream (optional): ASE / Fusion Detection
1. Chen Y, Li YI, Knowles DA, et al. Context-aware transcript quantification from long-read RNA-seq data with Bambu. Nat Methods. 2023;20(8):1187–1195. doi:10.1038/s41592-023-01908-w.  
2. Gilis J, Vitting-Seerup K, Baillie JK, et al. satuRn: Scalable analysis of differential transcript usage for bulk and single-cell RNA-sequencing applications. F1000Research. 2021;10:374. doi:10.12688/f1000research.51749.2.  
3. Langfelder P, Horvath S. WGCNA: an R package for weighted correlation network analysis. BMC Bioinformatics. 2008;9:559. doi:10.1186/1471-2105-9-559.  
4. Kerimov N, Hayhurst JD, Peat G, et al. eQTL Catalogue 2023: New datasets, X chromosome QTLs, and improved detection and visualisation of transcript-level QTLs. PLoS Genet. 2023;19(9):e1010932. doi:10.1371/journal.pgen.1010932.  
5. Newman AM, Steen CB, Liu CL, et al. Determining cell type abundance and expression from bulk tissues with digital cytometry. Nat Biotechnol. 2019;37(7):773–782. doi:10.1038/s41587-019-0114-2.  
6. White FM, Paull EO, Sinha P, et al. Community assessment of methods to deconvolve cellular composition from bulk gene expression. Nat Commun. 2024;15:7362. doi:10.1038/s41467-024-50618-0.  
7. D’Addabbo P, Nigita G, Locatelli F, et al. REDIportal: toward an integrated view of the A-to-I editing in human and mouse. Nucleic Acids Res. 2025;53(D1):D233–D242. doi:10.1093/nar/gkae1083.  
```

```markdown
# Downstream (optional): ASE / Fusion Detection
1. DePristo MA, Banks E, Poplin R, et al. A framework for variation discovery and genotyping using next-generation DNA sequencing data. Nat Genet. 2011;43(5):491–498. doi:10.1038/ng.806.  
2. Castel SE, Levy-Moonshine A, Mohammadi P, et al. Tools and best practices for data processing in allelic expression analysis. Nat Commun. 2016;7:12817. doi:10.1038/ncomms12817.  
3. Langfelder P, Horvath S. WGCNA: an R package for weighted correlation network analysis. BMC Bioinformatics. 2008;9:559. doi:10.1186/1471‑2105‑9‑559. 
4. Haas, B.J., Dobin, A., Li, B. et al. Accuracy assessment of fusion transcript detection via read-mapping and de novo fusion transcript assembly-based methods. Genome Biol 20, 213 (2019). https://doi.org/10.1186/s13059-019-1842-9 
5. Uhrig S, Schlee C, Lyu X, et al. Accurate and efficient detection of gene fusions from RNA sequencing data. Genome Res. 2021;31(3):448–460. doi:10.1101/gr.257246.119.
```

```markdown
# Workflow Engines, Automation & Reproducibility 
1. Backman TW, Girke T. systemPipeR: NGS workflow and report generation environment. BMC Bioinformatics. 2016;17(1). doi:10.1186/s12859-016-1241-0.  
2. Perelo S, Cornwell M, González I, et al. How tool combinations in different pipeline versions affect the outcome in RNA‑seq analysis. NAR Genomics and Bioinformatics. 2024;6(1):lqae020. doi:10.1093/nargab/lqae020.
3. Orjuela S, Huang R, Hembach KM, Robinson MD, Soneson C. ARMOR: An Automated Reproducible MOdular Workflow for Preprocessing and Differential Analysis of RNA‑seq Data. G3 (Bethesda). 2019;9(7):2089–2096. doi:10.1534/g3.119.400185.
4. Zhang P, Philippot Q, Ren W, et al. RASflow: an RNA‑Seq analysis workflow with Snakemake. BMC Bioinformatics. 2020;21:110. doi:10.1186/s12859‑020‑3433‑x.
5. Cornwell M, Vangala M, Taing L, Herbert Z, Köster J, Li B, et al. VIPER: Visualization Pipeline for RNA‑seq, a Snakemake workflow for efficient and complete RNA‑seq analysis. BMC Bioinformatics. 2018;19(1):135. doi:10.1186/s12859‑018‑2139‑9.
6. Eagles NJ, Lin L, Double B, et al. SPEAQeasy: a scalable pipeline for expression analysis and quantification for R/Bioconductor‑powered RNA‑seq analyses. BMC Bioinformatics. 2021;22:224. doi:10.1186/s12859‑021‑04142‑3.
```