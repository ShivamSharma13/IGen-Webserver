#!usr/bin/env python3
#Author: Deepali L. Kundnani
#Merges two vcf files: Keeping the Reference intact, extracts only Genotype column from Sample/subject vcf by matching rsids

import argparse
import subprocess
import pandas as pd
import os

parser = argparse.ArgumentParser(description='example: python3 merge.py -r Reference_samples_SNPS.vcf -t ./impute/hu6DB840_final.vcf -o imputemerge -c sample')
parser.add_argument('-r','--reference', required=True ,help='1000G Reference file w/o comments')
parser.add_argument('-t','--test', required=True , help='test vcf file before/after imputation')
parser.add_argument('-o','--out', required=True, help='Output folder/path')
parser.add_argument('-c','--col', required=True, help='Column name for Genotype information to be extracted from subject vcf file. ')
args = parser.parse_args()

print ("Reference File exists:"+str(os.path.exists(args.reference)))
print ("Subject File exists:" + str(os.path.exists(args.test)))

if os.path.exists(args.reference) and os.path.exists(args.test):

    #Removing comments from vcf files
    subprocess.call("grep -v '##' "+args.reference+" > reference.vcf", shell=True, universal_newlines=True)
    subprocess.call("grep -v '##' "+args.test+" > sample.vcf", shell=True, universal_newlines=True)
    
    #Taking in both sets of vcf files
    df=pd.read_csv('reference.vcf', sep='\t')
    sample=pd.read_csv('sample.vcf', sep='\t')
    
    #Merging only the genotype col from subject vcf file with the reference vcf based on rsids
    merge=df.merge(sample[['ID', args.col]], on="ID", how="inner")
    
    #Create output directory if it doesn't already exists
    if not os.path.exists(args.out):
        os.makedirs(args.out)
    #Saving merged.vcf file in the output directory
    merge.to_csv(args.out+'/'+'merged.vcf', sep='\t', index=False)
    print("Merged file saved in "+args.out+" directory as merged.vcf")
else:
    print("Please make sure the file names and location are correct")

