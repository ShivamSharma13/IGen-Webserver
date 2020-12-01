# IGen - Infections Genetics 
### An app that can give you relative risk estimates for multiple ommon Infections by looking at your personal Genome from different Direct To Consumer genetic testing companies

##### Merging subject vcf file to the 1000 Genomes Reference Dataset (Before Imputation for PCA and Population Stratification, After Imputation for PRS Score Calculations)

merge.py -

##### Imputation


##### List of Infections
Folder

##### From Imputed Vcf file to Getting the PRS scores
Extracting SNPs from the imputed subject vcf file pertaining to the Infections we are interested in
merge.py -

Generating PRS Score has follwoing two steps:
1. Getting Valid SNPs for every Infection by Clumping and Threshold using Plink
1. Getting PRS score for every Infection using the above Valid SNPs

PRS.py -

##### Percentile Calculation

percentile.py -
