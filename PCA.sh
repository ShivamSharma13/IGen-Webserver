#!/bin/bash

prefix=${1%%.*}

bgzip ${1}
tabix ${1}.gz

plink --vcf ${1}.gz --make-bed --pca --out ${2}/1000G_PCA_${prefix}
