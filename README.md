# scPathoQuant
The goal of this python package is to accurately align and quantify viral or bacterial (pathogen) derived reads for 10x single cell data.  This software integrates pathogen UMI counts and pathogen UMI gene counts into 10x files generated by first running [```cellranger count```](https://support.10xgenomics.com/single-cell-gene-expression/software/pipelines/latest/using/tutorial_ct) which aligns reads to your host genome of interest.  This generates output files for each sample such as features.tsv.gz and matrix.mtx.gz in the filtered_feature_bc_matrix and  raw_feature_bc_matrix folders. scPathoQuant then takes the unaligned reads from the host genome and maps them to your pathogen genome of interest and then integrates them back into the cellranger files.  This allows softwares such as seurat to be used for easy analysis of the data. The software uses outside software samtools, bowtie2, and htseq to quantify pathogen reads.  Default parameters are used when aligning reads to the pathogen genome and and non default htseq-count include using the --intersection-nonempty parameter.

### Dependencies
----------------
scPathoQuant requires **python 3.8 or greater** (tested on 3.8)

* pandas==2.0.3
* argparse==1.4.0
* htseq==2.0.5
* scipy==1.10.1
* seaborn==0.13.0
* pysam==0.22.0
* setuptools>=59.0.0
* matplotlib==3.3.2
* GFFUtils==0.12
* pyGenomeTracks==3.6

Currently only set to run on linux & mac but has only been tested on a linux platform

### Installation
----------------
Make sure pip version is 21.3.1 or greater  
Go into downloaded scPathoQuant folder and run the following commands

```bash
git clone https://github.com/galelab/scPathoQuant.git
cd ./scPathoQuant
pip install .
```

### Running scPathoQuant 
------------------------
Set the following parameters 
 
* -10x = Path/to/10x/sample/ (this the path to the output folder generated by first running [```cellranger count```](https://support.10xgenomics.com/single-cell-gene-expression/software/pipelines/latest/using/tutorial_ct) )
* -op = path/for/results 
* -p = number of processors (defualt = 1)
* -p2genome = path/to/pahogenreferencegenome/ - in this folder should be at most 2 files 1) the fasta file with the pathogen reference genome sequence and 2) pathogen gtf file (not mandatory this can just run with fasta file with the pathogen genome).  Note: In the fasta file the header will be used to quantify the number of pathogen total reads, it is recommended that if the fasta header is a complicated name it be simplified (i.e. > HIV_virus).  The Sars-CoV-2 reference genome and gtf file can be found in the data/sars-CoV2_reference_genome/ folder of this repository or can be found [here](https://www.ncbi.nlm.nih.gov/datasets/genome/GCF_009858895.2/)
* -align = alignment tool bbmap (default) or bowtie2
* -overwrite = will overwrite the files directly in the 10x filtered_feature_bc_matrix folder.  If not specified a copy of this folder will be made and then information about pathogen count information will be added to the files in this copied folder 
* --bbmap_params = parameters specific to the bbmap alignment tool  
* --bowtie2_params = parameters specific to the bowtie2 alignment tool
* --tmp_removal = if specified will remove the temporary directory (_tmp/) of files used by scpathoquant (these files can be large so if space is an issue these should be deleted)

Example runs:
```bash 
 scpathoquant -10x Path/to/10x/sample -op path/for/results -p 8 -p2genome path/to/pathogen/fastafilefolder/
```
```bash 
 scpathoquant -10x Path/to/10x/sample -op path/for/results -p 8 -p2genome path/to/pathogen/fastafilefolder/ --tmp_removal
```
```bash 
 scpathoquant -10x Path/to/10x/sample -op path/for/results -p 8 -p2genome path/to/pathogen/fastafilefolder --bbmap_params "--semiperfectmode"
```
```bash 
 scpathoquant -10x Path/to/10x/sample -op path/for/results -p 8 -p2genome path/to/viral/fastafilefolder  -align bowtie2 --bowtie2_params "--very-sensitive  --non-deterministic"
```

### Output files 
----------------
Output files by scPathoQuant

* pathogen_copy.png - violin plot showing number of cells with pathogen and UMI counts 
<img src="./pathogen_copy.png?raw=true" width="300"/>

* pathogen_genes.png - violin plot showing cells with pathogen gene UMI counts  
<img src="./pathogen_genes.png?raw=true" width="300"/>

* coveragemap.png - violin plot showing cells with pathogen gene UMI counts  
<img src="./coveragemap.png?raw=true" width="300"/>

* pathogen_al_counts.csv - total number of reads mapping to the pathogen in each cell 
* pathogen_al_gene_counts.csv - number of reads mapping to pathoen genes in each cell 
* pathogen_al.bam - reads mapped to pathogen
* pathogen_al_mapped.sam - reads mapped to only pathogen (no unmapped reads)
* pathogen_al_mapped_sort.bam - sorted reads mapped to pathogen (can be used to visualize reads in [IGV](https://www.igv.org/))
* pathogen_al_mapped_sort.bam.bai - index file to pathogen_al_sort.bam
* pathogen_al_mapped.fq.gz - fastq file of mapped reads to pathogens of interest.  Can be used to further perform phylogenetic and clade analyses 
* pathogen_al_sort_counts.sam - htseq output reads mapping to pathogen
* pathogen_genes_al_sort_counts.sam - htseq output reads mapping to individual pathogen genes (will not be produced if pathogen/viral gtf is not provided)
* Overwrites original 10x data provided to include pathogen counts and pathogen gene counts (if gtf file is provided)
* Path/to/10x/sample/outs/filtered_feature_bc_matrix_scPathoQuant_bbmap - files that can be integrated into seurat with pathogen counts 
* Path/to/10x/sample/outs/raw_feature_bc_matrix_scPathoQuant_bbmap - files that can be integrated into seurat with pathogen counts (this is not always needed)


### Loading data with pathogen counts into Seurat 
----------------------------------------------
Example seurat command in R
```bash 
seurat.object.data <- Read10X(data.dir ="Path/to/10x/sample/outs/filtered_feature_bc_matrix_scPathoQuant_bbmap")
```

### Output files in _tmp/ folder  
--------------------------------
Files in _tmp/ folder 
* unmmaped.bam - all unmapped reads from CellRanger (pulled from possorted_genome_bam.bam)
* unmmaped.sam - sam file generated from unmmaped.bam so that barcodes and umis can be extracted for unmmaped reds 
* barcodes_umi_read_table.csv - table of unmapped reads and corresponding barcodes and UMIs 
* unmapped.fq.gz - all unmapped reads in fastq format could be used fo downstream phylogentic analysis 

### Examples run codes 
----------------------
Examples and test data sets and codes for scPathoQuant can be found [here](https://github.com/galelab/Whitmore_scPathoQuant_testSets)

### CITATION
-------------
Whitmore LS, Tisoncik-Go J, Gale M Jr. scPathoQuant: a tool for efficient alignment and quantification of pathogen sequence reads from 10× single cell sequencing datasets. Bioinformatics. 2024 Mar 29;40(4):btae145. doi: 10.1093/bioinformatics/btae145. PMID: 38478395; PMCID: PMC10990681.

### LICENSE
----------------
BSD - 3-Clause Copyright 2023 University of Washington
