<!-- Editor guide
Use this file as a selectable reference bank for manuscript drafting.

Recommended use:

- Keep the section hierarchy aligned with natural manuscript sections: Introduction, Methods, Results/Discussion, data sharing, and acknowledgements.
- Treat each checkbox as a candidate citation rather than a guaranteed final citation.
- Keep only references that are actually used in the manuscript draft.
- Prefer primary sources for methods and high-quality reviews for broad background.
- When a project uses a specialized workflow (for example DIA, single-cell, spatial, or top-down proteomics), keep only the relevant optional subsection.
-->
Validated on `{{ validation_date }}` against the linked source pages.  

# 08_References

This file provides a curated reference bank for manuscript drafting, methods support, topic-specific background, and acknowledgements.  
*Use the checkboxes [x] to mark references that apply to the specific project before transferring them into the final manuscript bibliography.*

- [Introduction-Level Background](#introduction-level-background)
  - [General MS-Based Proteomics](#general-ms-based-proteomics)
  - [Quantitative and Label-Free Proteomics](#quantitative-and-label-free-proteomics)
- [Methods-Level References](#methods-level-references)
  - [Experimental Design, Reporting, and Standards](#experimental-design-reporting-and-standards)
  - [Data Processing, Quantification, and Statistics](#data-processing-quantification-and-statistics)
  - [Data Repositories and Reproducibility](#data-repositories-and-reproducibility)
- [Advanced or Alternative Workflow References](#advanced-or-alternative-workflow-references)
  - [DIA Proteomics](#dia-proteomics)
  - [Single-Cell Proteomics](#single-cell-proteomics)
  - [Spatial Proteomics](#spatial-proteomics)
  - [Top-Down Proteomics](#top-down-proteomics)
- [Topic-Specific Background for This Project](#topic-specific-background-for-this-project)
  - [Editor Guide](#editor-guide)
  - [System or Tissue Context](#system-or-tissue-context)
  - [Condition, Treatment, or Perturbation Context](#condition-treatment-or-perturbation-context)
  - [Project-Specific Biology](#project-specific-biology)
- [Candidate References for Results or Discussion Framing](#candidate-references-for-results-or-discussion-framing)
- [Iowa State University Cross-References](#iowa-state-university-cross-references)
  - [Protein Facility or Proteomics-Affiliated Publications](#protein-facility-or-proteomics-affiliated-publications)
  - [Bioinformatics Facility or Genome Informatics Facility Publications](#bioinformatics-facility-or-genome-informatics-facility-publications)
  - [Local Topic Context](#local-topic-context)
- [Acknowledgements](#acknowledgements)
  - [Facility Guidance](#facility-guidance)
  - [Example Acknowledgement Statements](#example-acknowledgement-statements)

## Introduction-Level Background

### General MS-Based Proteomics

⬜ Shuken SR. *An Introduction to Mass Spectrometry-Based Proteomics.* Journal of Proteome Research, 2023. Broad tutorial-style introduction suitable for readers outside proteomics. [PubMed](https://pubmed.ncbi.nlm.nih.gov/37260118/)
⬜ Aebersold R, Mann M. *Mass-spectrometric exploration of proteome structure and function.* Nature, 2016. Foundational review for the scope and biological value of modern MS proteomics. [Publisher](https://www.nature.com/articles/nature19949)
⬜ Guo T, Steen JA, Mann M. *Mass-spectrometry-based proteomics: from single cells to clinical applications.* Nature, 2025. Broad, up-to-date review for modern proteomics capabilities and future directions. [Publisher](https://www.nature.com/articles/s41586-025-08584-0) | [PubMed](https://pubmed.ncbi.nlm.nih.gov/40011722/)

### Quantitative and Label-Free Proteomics

⬜ *Liquid Chromatography-Mass Spectrometry-based Quantitative Proteomics.* Journal of Biological Chemistry, 2019. Overview of quantitative proteomics strategies and tradeoffs. [Publisher](https://www.jbc.org/article/S0021-9258%2819%2948534-7/fulltext)
⬜ *Experimental design and data-analysis in label-free quantitative LC-MS proteomics: A tutorial.* Journal of Proteomics, 2017. Useful for introducing design and statistical reasoning in LFQ studies. [PubMed](https://pubmed.ncbi.nlm.nih.gov/28391044/)
⬜ *Quantitative Mass Spectrometry-Based Proteomics: An Overview.* Methods in Molecular Biology, 2021. Useful when a general quantitative-proteomics methods citation is needed. [PubMed](https://pubmed.ncbi.nlm.nih.gov/33950486/)

## Methods-Level References

### Experimental Design, Reporting, and Standards

⬜ Taylor CF et al. *The minimum information about a proteomics experiment (MIAPE).* Nature Biotechnology, 2007. Standard reporting reference for proteomics experiments. [Publisher](https://www.nature.com/articles/nbt1329)
⬜ *Experimental Design in Quantitative Proteomics.* Methods in Molecular Biology, 2019. Useful when discussing replicates, bias prevention, and study structure. [PubMed](https://pubmed.ncbi.nlm.nih.gov/30980329/)
⬜ *Guidelines for Experimental Design and Data Analysis of Proteomic Mass Spectrometry-Based Experiments.* Amino Acids, 2010. Useful for methods justification in MS-based studies. [PubMed](https://pubmed.ncbi.nlm.nih.gov/20886359/)

### Data Processing, Quantification, and Statistics

⬜ Cox J, Mann M. *MaxQuant enables high peptide identification rates, individualized p.p.b.-range mass accuracies and proteome-wide protein quantification.* Nature Biotechnology, 2008. Foundational reference for a major bottom-up proteomics analysis platform. [PubMed](https://pubmed.ncbi.nlm.nih.gov/19029910/)
⬜ Cox J et al. *Accurate proteome-wide label-free quantification by delayed normalization and maximal peptide ratio extraction, termed MaxLFQ.* Molecular & Cellular Proteomics, 2014. Core LFQ quantification reference. [PubMed](https://pubmed.ncbi.nlm.nih.gov/24942700/) | [PMC](https://pmc.ncbi.nlm.nih.gov/articles/PMC4159666/)
⬜ Tyanova S et al. *The Perseus computational platform for comprehensive analysis of (prote)omics data.* Nature Methods, 2016. Useful for general downstream statistical and biological analysis citation. [PubMed](https://pubmed.ncbi.nlm.nih.gov/27348712/)
⬜ Benjamini Y, Hochberg Y. *Controlling the False Discovery Rate: A Practical and Powerful Approach to Multiple Testing.* Journal of the Royal Statistical Society Series B, 1995. Standard reference for FDR correction. [Publisher](https://rss.onlinelibrary.wiley.com/doi/10.1111/j.2517-6161.1995.tb02031.x)
⬜ *A systematic evaluation of normalization methods in quantitative label-free proteomics.* Briefings in Bioinformatics, 2018. Useful when normalization strategy needs literature support. [PubMed](https://pubmed.ncbi.nlm.nih.gov/27694351/)
⬜ *Computational Approaches in Proteomics.* Methods in Molecular Biology, 2020. Broad computational overview spanning acquisition, processing, and functional analysis. [PubMed](https://pubmed.ncbi.nlm.nih.gov/31815395/) | [NCBI Bookshelf](https://www.ncbi.nlm.nih.gov/books/NBK550333/)

### Data Repositories and Reproducibility

⬜ Vizcaíno JA et al. *ProteomeXchange provides globally coordinated proteomics data submission and dissemination.* Nature Biotechnology, 2014. Standard reference for public proteomics data deposition. [PubMed](https://pubmed.ncbi.nlm.nih.gov/24727771/) | [PMC](https://pmc.ncbi.nlm.nih.gov/articles/PMC3986813/)
⬜ *The ProteomeXchange consortium in 2026: making proteomics data FAIR.* Nucleic Acids Research, 2026. Up-to-date repository and reuse reference. [PMC](https://pmc.ncbi.nlm.nih.gov/articles/PMC12807779/)
⬜ Perez-Riverol Y et al. *The PRIDE database at 20 years: 2025 update.* Nucleic Acids Research, 2025. Useful when PRIDE is the destination repository or when discussing data accessibility. [PubMed](https://pubmed.ncbi.nlm.nih.gov/39494541/)

## Advanced or Alternative Workflow References

### DIA Proteomics

⬜ *Acquisition and Analysis of DIA-Based Proteomic Data.* Molecular & Cellular Proteomics, 2024. Use only if DIA acquisition or DIA-specific processing is relevant. [PubMed](https://pubmed.ncbi.nlm.nih.gov/38182042/) | [PMC](https://pmc.ncbi.nlm.nih.gov/articles/PMC10847697/)
⬜ *Data-Independent Acquisition: A Milestone and Prospect in Clinical Mass Spectrometry Proteomics.* Molecular & Cellular Proteomics, 2024. Optional second DIA review with stronger clinical emphasis. [PubMed](https://pubmed.ncbi.nlm.nih.gov/38880244/)

### Single-Cell Proteomics

⬜ *Initial recommendations for performing, benchmarking and reporting single-cell proteomics experiments.* Nature Methods, 2023. Use only for single-cell projects or when discussing emerging best practices. [PubMed](https://pubmed.ncbi.nlm.nih.gov/36864200/)
⬜ *Single-cell Proteomics: Progress and Prospects.* Molecular & Cellular Proteomics, 2021. Optional broad single-cell background review. [PubMed](https://pubmed.ncbi.nlm.nih.gov/32847821/)

### Spatial Proteomics

⬜ *Method of the Year 2024: spatial proteomics.* Nature Methods, 2024. Useful high-level context for tissue-resolved proteomics. [Publisher](https://www.nature.com/collections/dbifijbacd)
⬜ *An update on spatial proteomics.* Nature Methods, 2026. Optional current follow-up reference for projects using spatial methods. [Publisher](https://www.nature.com/articles/s41592-026-03046-5)
⬜ *Advances and Applications of Spatial Proteomics.* 2025 review. Useful for broader conceptual background beyond the Nature editorials. [PMC](https://pmc.ncbi.nlm.nih.gov/articles/PMC12800893/)

### Top-Down Proteomics

⬜ Habeck T, Lermyte F. *Seeing the complete picture: proteins in top-down mass spectrometry.* Essays in Biochemistry, 2023. Use only when top-down or proteoform-level analysis is relevant. [PubMed](https://pubmed.ncbi.nlm.nih.gov/36468679/)

## Topic-Specific Background for This Project

<!-- Editor Guide

Use this section to collect references that explain the specific biological system, tissue, treatment, perturbation, or disease context of the project.

What to include:

- 1 to 3 broad review papers that explain the system or tissue being studied
- 1 to 3 references that explain the main treatment, perturbation, disease, or exposure
- 1 to 3 papers that connect the biological context specifically to proteomics, when available
- optional organism-specific or field-standard background references that are likely to be cited in the Introduction or Discussion

What to prefer:

- current high-quality reviews for broad context
- primary papers when a specific mechanism, treatment, or phenotype is central to the project
- papers that match the organism, tissue, and study design as closely as possible

What to avoid:

- references that are only locally relevant but not scientifically useful for the manuscript
- generic omics citations when the section needs system-specific biology
- project-irrelevant examples carried over from a previous template use

### System or Tissue Context

⬜ `{{ system_or_tissue_reference_1 }}`
⬜ `{{ system_or_tissue_reference_2 }}`
⬜ `{{ system_or_tissue_reference_3 }}`

### Condition, Treatment, or Perturbation Context

⬜ `{{ condition_or_treatment_reference_1 }}`
⬜ `{{ condition_or_treatment_reference_2 }}`
⬜ `{{ condition_or_treatment_reference_3 }}`

### Project-Specific Biology

⬜ `{{ project_specific_reference_1 }}`
⬜ `{{ project_specific_reference_2 }}`
⬜ `{{ project_specific_reference_3 }}`

-->

## Candidate References for Results or Discussion Framing

⬜ *Robust, reproducible and quantitative analysis of thousands of proteomes by micro-flow LC–MS/MS.* Nature Communications, 2020. Useful if throughput, robustness, or reproducibility of LC-MS workflows is discussed. [Publisher](https://www.nature.com/articles/s41467-019-13973-x)
⬜ *What have Data Standards ever done for us?* 2025 review. Useful only if the manuscript discusses reproducibility, data standards, or reuse. [PubMed](https://pubmed.ncbi.nlm.nih.gov/40024375/)
⬜ *The Importance, Challenges, and Possible Solutions for Sharing Proteomics Data.* 2024 review. Useful if open-data practice or repository use is discussed. [PMC](https://pmc.ncbi.nlm.nih.gov/articles/PMC10915627/)

## Iowa State University Cross-References

These are optional Iowa State University-affiliated publications that may be useful when local facility context, institutional precedent, or related analytical work should be cited. They are not required for every manuscript, but they can help connect the project to relevant ISU expertise and prior proteomics or bioinformatics work.

### Protein Facility or Proteomics-Affiliated Publications

⬜ Kim W. *Soybean seed proteomics: Methods for the isolation, detection, and identification of low abundance proteins.* Methods in Molecular Biology, 2023. Author affiliation includes the Protein Facility of the Iowa State University Office of Biotechnology; useful as an ISU-affiliated proteomics methods citation. [PubMed](https://pubmed.ncbi.nlm.nih.gov/36280356/)
⬜ Patel KR et al. *Primary Human Natural Killer Cells Retain Proinflammatory IgG1 at the Cell Surface and Express CD16a in a Conformation That Is Susceptible to Shedding.* Molecular & Cellular Proteomics, 2019. Includes Iowa State University Protein Facility affiliation; useful as an example of ISU-affiliated proteomics application work. [PubMed](https://pubmed.ncbi.nlm.nih.gov/31467031/)

### Bioinformatics Facility or Genome Informatics Facility Publications

⬜ Bagheri H, Severin AJ, Rajan H. *Detecting and correcting misclassified sequences in the large-scale public databases.* Bioinformatics, 2020. Includes Genome Informatics Facility affiliation; useful only when discussing general ISU bioinformatics expertise, not as a core citation for a proteomics manuscript. [PubMed](https://pubmed.ncbi.nlm.nih.gov/32579213/)

### Local Topic Context

⬜ `{{ local_relevant_reference_1 }}`
⬜ `{{ local_relevant_reference_2 }}`

## Acknowledgements

### Facility Guidance

> The Office of Biotechnology FAQ states that presentations and manuscripts using data generated from Office of Biotechnology facilities must, at minimum, acknowledge the name of the facility. [Official page](https://www.biotech.iastate.edu/faq/)

> The Bioinformatics Facility provides explicit acknowledgement language on its FAQ page. [Official page](https://www.biotech.iastate.edu/bioinformatics/gif-faq/)

### Example Acknowledgement Statements

**Protein Facility acknowledgement**

```text
We acknowledge the Iowa State University Protein Facility in the Office of Biotechnology for proteomics sample processing and mass spectrometry support.
```

**Bioinformatics Facility acknowledgement**

```text
We gratefully acknowledge the Bioinformatics Facility in the Office of Biotechnology at Iowa State University for their comprehensive bioinformatics analyses.
```

**Acknowledgement with staff support**

```text
We thank the Office of Biotechnology core facilities and staff for their technical assistance and support.
```

**Broader Iowa State University acknowledgement**

```text
We thank the Office of Biotechnology at Iowa State University for providing core-facility infrastructure, advanced instrumentation, and staff expertise that supported this work.
```
