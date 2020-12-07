#!/bin/bash 

cd /projects/team-2/html/biol-8803-IGen/IGenWebServer/pipeline-scripts

gunzip ${2}/inputfile_filtered.gz
python3 merge.py -r ${3} -t ${2}/inputfile_filtered -o ${2}/post_knn_merge -c ${1}
