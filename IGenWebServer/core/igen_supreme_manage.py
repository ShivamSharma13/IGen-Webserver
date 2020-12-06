import subprocess
import logging

def supreme_manager(user_home_dir, user_vcf_file_path, dna_service_provider, log_file_path):
	log_file_path = os.path.join(user_home_dir, str(prs_object.uuid), "pipeline.log")
	logging.basicConfig(filename=log_file_path, filemode='a', format='[%(levelname)s] - %(message)s', level=logging.INFO)
	logging.info('Reached supreme manager.')

	#Sara Imputation.
	subprocess.call("../pipeline-scripts/inputfiletype.sh " + dna_service_provider + " " + user_vcf_file_path + " " + os.path.join(user_home_dir, str(prs_object.uuid)), shell = True)
