#!/bin/bash

# inputs in this order: 
# {1} target folder

nsv=1000
cd ${1}

for i in `ls *.matrix`
do 
	#echo $i
	nrow=$(wc -l < ${i%.matrix})
	echo $nrow
	echo $i
	echo "/projects/slin_prj/slin_prj_results/Medline/debugging/runningGraphlab/pubmed_svd.sh $i $nsv $nrow . > $i.log"
	
	/projects/slin_prj/slin_prj_results/Medline/debugging/runningGraphlab/pubmed_svd.sh $i $nsv $nrow . > $i.log
	mv out.$nsv.U.1_of_1 $i.U
	mv out.$nsv.singular_values $i.S
done