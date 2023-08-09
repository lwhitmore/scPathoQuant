# scViralQuant
The goal of this python package is to accurately align and quantify viral reads for 10x single cell data.  This software integrates viral UMI counts and viral UMI gene counts into 10x files generated by first running [```cellranger count```](https://support.10xgenomics.com/single-cell-gene-expression/software/pipelines/latest/using/tutorial_ct) which aligns reads to your host genome of interest.  This generates output files for each sample such as features.tsv.gz and matrix.mtx.gz in the filtered_feature_bc_matrix and  raw_feature_bc_matrix folders. scViralQuant then takes the unaligned reads from the host genome and maps them to your viral genome of interest and then integrates them back into the cellranger files.  This allows softwares such as seurat to be used for easy analysis of the data. The software uses outside software samtools, bowtie2, and htseq to quantify viral reads.  Default parameters are used when aligning reads to the viral genome and and non default htseq-count include using the --intersection-nonempty parameter.

### Dependencies
----------------
scViralQuant is tested to work in python 3.6.8

* argsparse
* htseq
* pandas 
* scipy
* pysam
* seaborn

Currently only set to run on linux & mac but has only been tested on a linux platform

### Installation
----------------
Go into downloaded scViralQuant folder and run the following commands

```bash
cd ./scViralQuant
pip install -r requirements.txt
python setup.py install
```

### Running scViralQuant 
------------------------
Set the following parameters 
 
* -10x = Path/to/10x/sample/ (this the path to the output folder generated by first running [```cellranger count```](https://support.10xgenomics.com/single-cell-gene-expression/software/pipelines/latest/using/tutorial_ct) )
* -op = path/for/results 
* -p = number of processors (defualt = 1)
* -p2genome = path/to/viralreferencegenome/ - in this folder should be at most 2 files 1) the fasta file with the viral genome sequence and 2) viral gtf file (not mandatory this can just run with fasta file with the viral genome).  Once bowtie2 indexes are made folder can be reused with out having to remake bowtie indexes.  Note: In the fasta file the header will be used to quantify the number of viral copies, it is recommended that if the fasta header is a complicated name it be simplified (i.e. > HIV_virus).  The Sars-CoV-2 reference genome and gtf file can be found in the data/sars-CoV2_reference_genome/ folder of this repository or can be found [here](https://www.ncbi.nlm.nih.gov/datasets/genome/GCF_009858895.2/)
* -align = alignment tool bbmap (default) or bowtie2
* -overwrite = will overwrite the files directly in the 10x filtered_feature_bc_matrix folder.  If not specified a copy of this folder will be made and then information about viral count information will be added to the files in this copied folder 
* --bbmap_params = parameters specific to the bbmap alignment tool  
* --bowtie2_params = parameters specific to the bowtie2 alignment tool
* --tmp_removal = if specified will remove the temporary directory (_tmp/) of files used by scviralquant (these files can be large so if space is an issue these should be deleted)

Example runs:
```bash 
 scviralquant -10x Path/to/10x/sample -op path/for/results -p 8 -p2genome path/to/viral/fastafilefolder
```
```bash 
 scviralquant -10x Path/to/10x/sample -op path/for/results -p 8 -p2genome path/to/viral/fastafilefolder --tmp_removal
```
```bash 
 scviralquant -10x Path/to/10x/sample -op path/for/results -p 8 -p2genome path/to/viral/fastafilefolder --bbmap_params "--semiperfectmode"
```
```bash 
 scviralquant -10x Path/to/10x/sample -op path/for/results -p 8 -p2genome path/to/viral/fastafilefolder  -align bowtie2 --bowtie2_params "--very-sensitive  --non-deterministic"
```

### Output files 
----------------
Output files by scViralQuant

* viral_copy.png - violin plot showing number of cells with virus and UMI counts 
<img src="./viral_copy.png?raw=true" width="300"/>

* viral_genes.png - violin plot showing cells with viral gene UMI counts  
<img src="./viral_genes.png?raw=true" width="400"/>

* virus_al_counts.csv - total number of reads mapping to the virus in each cell 
* virus_al_gene_counts.csv - number of reads mapping to viral genes in each cell 
* virus_al.bam - reads mapped to virus (no unmapped reads)
* virus_al_mapped.sam - reads mapped to only virus (no unmapped reads)
* virus_al_sort.bam - sorted reads mapped to virus 
* virus_al_sort.bam.bai - index file to virus_al_sort.bam
* virus_al_sort_counts.sam - htseq output reads mapping to virus
* virus_genes_al_sort_counts.sam - htseq output reads mapping to individual virus genes (will not be produced if viral gtf is not provided)
* Overwrites original 10x data provided to include viral counts and viral gene counts (if gtf file is provided)
* Path/to/10x/sample/outs/filtered_feature_bc_matrix_bbmap - files that can be integrated into seurat with viral counts 
* Path/to/10x/sample/outs/raw_feature_bc_matrix_bbmap - files that can be integrated into seurat with viral counts (this is not always needed)

### Loading data with viral counts into Seurat 
----------------------------------------------
Example seurat command in R
```bash 
seurat.object.data <- Read10X(data.dir ="sampleofinterest/outs/filtered_feature_bc_matrix_bbmap")
```

### CITATION
-------------
scViralQuant: A tool for efficient alignment and quantification of viral reads from 10x single cell sequencing data sets
Leanne S. Whitmore, Jennifer Tisoncik-Go, Michael Gale Jr.
bioRxiv 2023.07.21.549987; doi: https://doi.org/10.1101/2023.07.21.549987

### LICENSE
----------------
BSD - 3-Clause Copyright 2023 University of Washington
