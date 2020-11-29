import argparse
import subprocess
from multiprocessing import Pool 

parser=argparse.ArgumentParser()
parser.add_argument("-i", required=True)
parser.add_argument("-t", required=True)
args=parser.parse_args()

#convert 23andme file to vcf 
subprocess.call(["bcftools", "convert", "--tsv2vcf", args.i, "-f", "Homo_sapiens.GRCh37.75.dna.primary_assembly.fa","-s", args.i, "-Ov", "-o", args.i + ".vcf"])

#remove duplicate locations in vcf 
subprocess.call(["bcftools", "norm", "-d", "both", "-O", "v", "-o", args.i + "_noduplicates.vcf",  args.i + ".vcf"])

#remove rsids with missing ref or alt alleles 
output=open(args.i + "_filtered","w")
with open(args.i + "_noduplicates.vcf", "r") as fh:
	for line in fh:
		if line.startswith("#"):
			output.write(line)
		else:
			line1=line.strip()
			row=line1.split("\t")
			print(row)
			if row[3]=="." or row[4]==".":
				pass
			else: 
				output.write(line)

#zip vcf file 
subprocess.call(["bgzip", args.i + "_filtered"])

#index input vcf file 
subprocess.call(["tabix", args.i + "_filtered.gz"])


#phasing 23andme vcf file by chromosome 
def phase(ref, chr):
	subprocess.call(["tabix", "Phase_References/" + ref])
	subprocess.call(["Eagle2/Eagle_v2.4.1/eagle", "--vcfTarget", args.i + "_filtered.gz", "--vcfRef","Phase_References/" + ref, "--geneticMapFile", "Eagle2/Eagle_v2.4.1/tables/genetic_map_hg19_withX.txt.gz", "--outPrefix", "eagleoutput/" + args.i + "_eagle" + chr, "--chrom", chr])
	#converting output vcf file to ped file 
	subprocess.call(["vcftools", "--gzvcf", "eagleoutput/" + args.i + "_eagle" + chr + ".vcf.gz", "--out", "eagleoutput/" + args.i + "_eagle" + chr,  "--plink"])
	#converting ped file to gen file 
	subprocess.call(["gtool", "-P", "--ped", "eagleoutput/" + args.i + "_eagle" + chr + ".ped","--map", "eagleoutput/" + args.i + "_eagle" + chr + ".map"])



#phasing gen file from phasing function in 1,000,000 bp sections 
def impute(map, hap, legend, int_start, int_end, order, chr):
	subprocess.call(["impute2", "-m", map, "-h", hap, "-l",legend, "-g", "eagleoutput/" + args.i + "_eagle" + str(chr) + ".ped" + ".gen", "-int", str(int_start), str(int_end), "-Ne", "20000", "-o","imputeoutput/" + args.i + "_impute" + str(chr) + "_" + str(order)])

chrlist=[2,3,6,7,8,12,17,19]
phaselist=[]


#create phaselist for multiprocessing
for i in chrlist:
        i=str(i)
        phaselist.append(("ALL.chr" + i + ".phase3.bcf.gz", i))


map_loc="1000GP_Phase3/genetic_map_chr"
hap_loc="1000GP_Phase3/1000GP_Phase3_chr"
legend_loc="1000GP_Phase3/1000GP_Phase3_chr"

map_2, hap_2, legend_2 = map_loc + "2_combined_b37.txt", hap_loc + "2.hap.gz", legend_loc + "2.legend.gz"
map_3, hap_3, legend_3 = map_loc + "3_combined_b37.txt", hap_loc + "3.hap.gz", legend_loc + "3.legend.gz"
map_6, hap_6, legend_6 = map_loc + "6_combined_b37.txt", hap_loc + "6.hap.gz", legend_loc + "6.legend.gz"
map_7, hap_7, legend_7 = map_loc + "7_combined_b37.txt", hap_loc + "7.hap.gz", legend_loc + "7.legend.gz"
map_8, hap_8, legend_8 = map_loc + "8_combined_b37.txt", hap_loc + "8.hap.gz", legend_loc + "8.legend.gz"
map_12, hap_12, legend_12 = map_loc + "12_combined_b37.txt", hap_loc + "12.hap.gz", legend_loc + "12.legend.gz"
map_17, hap_17, legend_17 = map_loc + "17_combined_b37.txt", hap_loc + "17.hap.gz", legend_loc + "17.legend.gz"
map_19, hap_19, legend_19 = map_loc + "19_combined_b37.txt", hap_loc + "19.hap.gz", legend_loc + "19.legend.gz"


imputelist=[]
count=0

#create impute list for multiprocessing 
def chr_ranges(start, end, count, map, hap, legend, chr):
	current_start=start
	current_end=start+1000000
	while current_start<=end: 
		count+=1
		imputelist.append((map, hap, legend, current_start, current_end, count, chr))
		current_start+=1000000
		current_end+=1000000
	return count 


count= chr_ranges(63096701, 64393884, count, map_2, hap_2, legend_2, 2)
count= chr_ranges(49004426, 50124246, count, map_3, hap_3, legend_3, 3)
count= chr_ranges(134954, 40360207, count, map_6, hap_6, legend_6, 6)
count= chr_ranges(51855106, 56130723, count, map_6, hap_6, legend_6, 6)
count= chr_ranges(63827870, 67396070, count, map_6, hap_6, legend_6, 6)
count= chr_ranges(78951423, 88728609, count, map_6, hap_6, legend_6, 6)
count= chr_ranges(98365774, 99480656, count, map_6, hap_6, legend_6, 6)
count= chr_ranges(107725731, 134308077, count, map_6, hap_6, legend_6, 6)
count= chr_ranges(144017968, 147885413, count, map_6, hap_6, legend_6, 6)
count= chr_ranges(159534234, 167440312, count, map_6, hap_6, legend_6, 6)
count= chr_ranges(68608301, 69969629, count, map_7, hap_7, legend_7, 7)
count= chr_ranges(99569546, 101142116, count, map_8, hap_8, legend_8, 8)
count= chr_ranges(99212368, 99937609, count, map_12, hap_12, legend_12, 12)
count= chr_ranges(17411801, 18245166, count, map_17, hap_17, legend_17, 17)
count= chr_ranges(39430913, 40002820, count, map_19, hap_19, legend_19, 19)
count= chr_ranges(48811043, 49662512, count, map_19, hap_19, legend_19, 19)



#calling phase and impute functions with multiprocessing 
pool=Pool(int(args.t))
list(pool.starmap(phase, phaselist))
#list(pool.starmap(impute, imputelist))

