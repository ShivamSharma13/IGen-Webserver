import subprocess
import logging

def supreme_manager(user_project_dir, user_vcf_file_path, dna_service_provider):
	#Sara Imputation.
	subprocess.call("../pipeline-scripts/inputfiletype.sh " + dna_service_provider + " " + user_vcf_file_path + " " + user_project_dir, shell = True)
