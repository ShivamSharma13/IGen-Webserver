import subprocess
import logging
import argparse
import os

def supreme_manager(user_project_dir, user_vcf_file_path, dna_service_provider):
	#Sara Imputation.
	print("Calling inputfiletype.sh ...")
	#subprocess.call("../pipeline-scripts/inputfiletype.sh " + dna_service_provider + " " + user_vcf_file_path + " " + user_project_dir, shell = True)

	#Merge file.
	print("Performing PCA ...")	
	#subprocess.call("../pipeline-scripts/masterPCA.sh " + user_vcf_file_path + " " + user_project_dir, shell = True)

	#Get the PCA Token.
	with open(os.path.join(user_project_dir, "token_s_d.txt")) as f:
		raw = f.read()

	token = [i for i in raw.split("\n")][0]

	reference_token_file_for_merge = os.path.join("/projects/team-2/html/lib", token + "_Reference.vcf")
	subprocess.call("../pipeline-scripts/post_pca.sh " + user_vcf_file_path + " " + user_project_dir + " " + reference_token_file_for_merge, shell=True)

	return

if __name__ == "__main__":
	parser = argparse.ArgumentParser()

	#Arguments.
	parser.add_argument("-i", "--input-file", help="Enter VCF file path.", required=False)
	parser.add_argument("-o", "--output-dir", help="Output directory.", required=False)
	parser.add_argument("-d", "--dna-service", help="DNA Service.", required=False)

	#Parse and gather whatever the user sent.
	args = vars(parser.parse_args())
	vcf_file_path = args['input_file']
	output_dir = args['output_dir']
	dna_service = args['dna_service']

	supreme_manager(output_dir, vcf_file_path, dna_service)