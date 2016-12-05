#!/bin/bash

# inputs in this order: 
# {1} target folder
# {2} outfolder  

for i in `ls ${1}`
do 
	f=${1}/$i
	out=${2}/$i
	echo $out
	echo $f
	python /projects/slin_prj/slin_prj_results/PubMed_Experiment/random_100_pubmed/code/tf_idf.py --t $f --tfidf $out
done