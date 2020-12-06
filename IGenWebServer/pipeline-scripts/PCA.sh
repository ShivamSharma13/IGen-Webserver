#!/bin/bash

#first argument is unique output location 

bgzip merged.vcf 
tabix merged.vcf.gz

plink --vcf merged.vcf.gz --make-bed --pca --out ${1}/PCA/1000G_PCA_merged
