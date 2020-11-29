#!/bin/bash

python3 imputation_pipeline.py -i $1 -t $2

python3 impute2temp.py -i $1

./temp2vcf.sh $1

rm ${1}_filtered.gz ${1}_filtered.gz.tbi ${1}_noduplicates.vcf 
