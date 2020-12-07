#!/bin/bash

#first argument is unique output location 

bgzip ${1}/merged.vcf 
tabix ${1}/merged.vcf.gz

plink --vcf ${1}/merged.vcf.gz --make-bed --pca --out ${1}/PCA/1000G_PCA_merged
