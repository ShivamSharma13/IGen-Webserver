#!/usr/bin/env python3
import argparse
import subprocess
import re 
from multiprocessing import Pool

parser=argparse.ArgumentParser()
parser.add_argument("-i", required=True)
args=parser.parse_args()

subprocess.call(["rm", "-r", "imputetemp/"])
subprocess.call(["mkdir", "imputetemp"])

def openfile(filename, chr):
	tempoutput=open("imputetemp/" + args.i + "-" + str(chr) + "_impute_filtered", "a")
	rsidfile=open("imputetemp/rsidfile" + str(chr), "a")
	with open("imputeoutput/" + filename, "r") as fh:
		for line in fh:
			if line.startswith("--- rs"):
				tempoutput.write(line)
				row=line.split(" ")
				row[1]=row[1].split(":")
				rsidfile.write(row[1][0] + "\t" + row[1][1] + "\n")
			#if re.search("^[0-9]",line):
			#	row=line.split(" ")
			#	templine="--- " + row[1] + ":" + row[2] + ":" + row[3] + ":" + row[4] + " " + row[2] + " " + row[3] + " " + row[4] + "\n"
			#	tempoutput.write(templine)
			#	rsidfile.write(row[1] + "\t" + row[2])

openfile(args.i + "_impute2_1", 2)
openfile(args.i + "_impute2_2", 2)
openfile(args.i + "_impute3_3", 3)
openfile(args.i + "_impute3_4", 3)
openfile(args.i + "_impute7_106", 7)
openfile(args.i + "_impute7_107", 7)
openfile(args.i + "_impute8_108", 8)
openfile(args.i + "_impute8_109", 8)
openfile(args.i + "_impute12_110", 12)
openfile(args.i + "_impute17_111", 17)
openfile(args.i + "_impute19_112", 19)
openfile(args.i + "_impute19_113", 19)

for i in range(5, 106):
	openfile(args.i + "_impute6_" + str(i), 6)

chrlist=[2,3,6,7,8,12,17,19]
for chr in chrlist:			
	sampleoutput=open("imputetemp/" + args.i + "-" + str(chr) + "_awk.samples", "w")
	sampleoutput.write(args.i)

