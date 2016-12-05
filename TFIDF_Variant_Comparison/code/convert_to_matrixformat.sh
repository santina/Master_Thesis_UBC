#!/bin/bash

# inputs in this order: 
# {1} target folder

for i in `ls ${1}/*.tf`
do 
	
	out=$i.matrix
	echo $out
	echo $i
	python /projects/slin_prj/slin_prj_results/PubMed_Experiment/random_100_pubmed/code/convert_format.py --t $i --m $out
done