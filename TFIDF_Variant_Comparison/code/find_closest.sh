#!/bin/bash

# inputs in this order: 
# {1} target folder (tf variant)
# {2} pmids folder
# {3} meta folder
# {4} log folder
# {5} outfolder


for i in `ls ${1}/*.matrix`
do 
	# strip out 
	
	i=${i##*/} # strip out folder name 

	U=${1}/$i.U
	S=${1}/$i.S
	out=${5}/${1}/${i%%.*}
	mkdir $out

	pmids=${2}/${i%%.*}  # trip everything after the first . 
	meta=${3}/${i%.tf.matrix}
	log=${4}/${i%.all.tf.matrix}.log
	nrow=$(wc -l < ${1}/${i%.matrix})
	
	echo $U
	echo $S
	echo $out
	echo $pmids
	echo $meta
	echo $log
	echo $nrow


	python /projects/slin_prj/slin_prj_results/PubMed_Experiment/random_100_pubmed/code/find_closest_papers.py \
	--category $pmids --meta $meta --npaper $log \
	--nsv 1000 --step 50 --start 50 --nrow $nrow \
	--m $U --s $S --out $out

	

done