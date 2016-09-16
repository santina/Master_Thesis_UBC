#!/bin/bash 

# Call this script with these parameters in order: 
# folder with folders of abstract files 

folders=$(ls ${1})
for folder in $folders
do 
	folderpath=${1}/$folder
	outfile=$folderpath/$folder".all"
	echo $folderpath
	echo $outfile
	python \
	/projects/slin_prj/slin_prj_results/PubMed_Experiment/random_100_pubmed/code/concate.py \
	--f $folderpath --out $outfile

done

