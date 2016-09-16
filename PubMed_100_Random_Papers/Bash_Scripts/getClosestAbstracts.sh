#!/bin/bash 

# Call this script with these parameters in order: 
# folder with ID files, outfolder name, email

IDfiles=$(ls ${1})
for item in $IDfiles
do 

	IDfile=${1}/$item
	outfolder=${2}/$item
	mkdir $outfolder
	log=${2}/$item/$item".log"

	echo $outfolder

	python \
	/projects/slin_prj/slin_prj_results/PubMed_Experiment/random_100_pubmed/code/getClosestAbstracts.py \
	--f $IDfile --a $outfolder --e $log --email ${3}

done