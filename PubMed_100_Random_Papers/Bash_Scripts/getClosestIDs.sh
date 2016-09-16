#!/bin/bash 

# Call this script with these parameters in order: 
# foldername, basefilename, outfolder, email



#foldername='/projects/slin_prj/PubMed_Experiment/random_100_pubmed_repeats/random_pmids'
#basefilename='100_randomIDs_'


for i in $(seq 0 99)
do 
	filename=${1}/${2}$i
	outfile=${3}/${2}$i.neighbors
	python ../code/getClosestIDs.py --f $filename --out $outfile --email ${4}
done 