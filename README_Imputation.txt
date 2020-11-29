Reference files needed: 
1000GP_Phase3 folder 
Phase_References folder 
Homo_sapiens.GRCh37.75.dna.primary_assembly.fa
Homo_sapiens.GRCh37.75.dna.primary_assembly.fa.fai 

Tools needed: 
eagle2 -- not in conda 
gtool -- not in conda 
plink
impute2 
bcftools 
vcftools 
bgzip -- should be in bin folder 
tabix -- should be in bin folder 

inputfiletype.sh
two inputs needed: file type (1st input) file name (2nd input)
This script will convert the input file to 23andMe format and call masterscript.sh

masterscript.sh
one input needed: file name (in 23andMe format)
calls three scripts: imputation_pipeline.py, impute2temp.py, temp2vcf.sh

imputation_pipeline
one input needed: file name (in 23andMe format)
Threading is hardcoded, but you can change the number of threads in inputefiletype.sh
output: gen file 

impute2temp.py 
one input needed: file name 
concatenates impute files by chromosome, extracts rsids from each file, filters file to only include lines with rsids 

temp2vcf.py 
one input needed: file name 
takes imputed filtered files and outputs a singular vcf for PRS calculation 


