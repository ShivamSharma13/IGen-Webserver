#!usr/bin/env python3
#Author: Deepali L. Kundnani
#Uses the merged vcf file after imputation and summary statistics files for different infections to calculate PRS scores with output in one folder and percentile results in another

import argparse
import subprocess
import os
import pandas as pd  #requires pip install pandas 
import numpy as np    #requires pip install pandas or numpy
from scipy import stats   #requires pip install scipy

parser = argparse.ArgumentParser(description='example: python3 PRS.py -s ~/scratch/stats/Infections -m ~/scratch/merge/mergedforPRS.vcf -o ~/scratch/stats/PRS -r ~/scratch/stats/percentile -c INFO_y')
parser.add_argument('-s','--SNP', required=True ,help='full path to folder with summary statitics')
parser.add_argument('-m','--merged', required=True , help='full path of merged vcf files after imputation')
parser.add_argument('-o','--out', required=True, help='Output folder/path(full path)')
parser.add_argument('-r','--results', required=True, help='Results folder/path(full path)')
parser.add_argument('-c','--col', required=True, help='Column name for Genotype information to be extracted from subject vcf file. ')
args = parser.parse_args()

def PRS(statloc,output,filename,basename):
    subprocess.call("awk '{print $2,$7}' '"+statloc+"/"+filename+"' > "+basename+".snp.pvalue", shell=True, universal_newlines=True)
    subprocess.call("plink --bfile final --clump-kb 250 --clump '"+statloc+"/"+filename+"' --clump-snp-field SNP --clump-field P --out "+basename+" ", shell=True, universal_newlines=True)
    if os.path.exists(output+basename+'.clumped'):
        subprocess.call("awk 'NR!=1{print $3}' "+basename+".clumped > "+basename+".valid.snp", shell=True, universal_newlines=True)
        subprocess.call("plink --bfile final --score "+statloc+"/"+filename+" 2 5 8 header sum --extract "+basename+".valid.snp -out "+basename+" ", shell=True, universal_newlines=True)
    else:
        subprocess.call("plink --bfile final --score "+statloc+"/"+filename+" 2 5 8 header -out "+basename+" ", shell=True, universal_newlines=True)

def percentile(output,basename,name):
    ID=[] #list of IDs of population
    Score=[]   #list of scores of population
    f=open(output+'/'+basename+'.profile', "r")
    header=f.readline()
    header=header.split()
    x=header.index('FID') #column for ID
    y=header.index('SCORE')   #column for Score
    for lines in f:
        line=lines.split()
        if line[0]==name:
            sampleID=line[x]   #Sample ID
            sampleScore=float(line[y])   #Sample score
        else:
            ID.append(line[x])
            Score.append(float(line[y]))
    
    f.close()
    ### Calculating Percentile of the Sample score in the list of scores for the population
    percentile = int(stats.percentileofscore(Score, sampleScore))
    return(percentile)


#Create output directory if it doesn't already exists
if not os.path.exists(args.out):
    os.makedirs(args.out)
if not os.path.exists(args.results):
    os.makedirs(args.results)

print ("SNP folder exists:" + str(os.path.exists(args.SNP)))
print ("Merged File exists:" + str(os.path.exists(args.merged)))


###Converting the Vcf file to different plink compatible formats in the output directory
os.chdir(args.out)

subprocess.call("vcftools --vcf "+args.merged+" --plink --out final", shell=True, universal_newlines=True)
subprocess.call("plink --file final --make-bed --out final", shell=True, universal_newlines=True)
subprocess.call("plink --bfile final --maf 0.01 --mind 0.01 --write-snplist --make-just-fam --out final", shell=True, universal_newlines=True)

#Getting the list of all the infection files existing in the specified folder
Infections=os.listdir(args.SNP)
Infections.sort()

###Calculating PRS and getting the percentile for every infection
if os.path.exists(args.SNP):
    for infection in Infections:
        infect=infection.split('.')[0]
        inf=infect.replace("_", " ")
        
        # Clumping and Calculating PRS score
        PRS(args.SNP,args.out,infection,infect)
        
        #Calculating percentile for each infection from the PRS scores file
        perc=percentile(args.out,infect,args.col)
        perc=str(perc)
        
        #Create percentiles.txt if it doesn't exist in the results folder
        if os.path.exists(args.results+'/percentiles.txt'):
            subprocess.call("rm "+args.results+"/percentiles.txt",shell=True, universal_newlines=True)
        else:
            subprocess.call("touch "+args.results+"/percentiles.txt",shell=True, universal_newlines=True)
            
        #Append your infection name and percentile risk/score for the individual in the results folder under percentiles.txt
        subprocess.call("echo "+inf+"\t"+perc+">>"+args.results+"/percentiles.txt", shell=True, universal_newlines=True)
        
else:
    print("Please make sure the file names and location are correct")
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    


