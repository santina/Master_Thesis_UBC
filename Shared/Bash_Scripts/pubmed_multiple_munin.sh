#!/bin/bash

# input in this order:
# {1} target folder
# {2} filename prefix matching (ex: random_pmid_1 will match to random_pmid_{1,12,11,13,...}) to breakdown our calls
# {3} # singular values
# {4} # output folder

matrixFiles=$(ls ${1})
for file in $matrixFiles
do
	if [[ $file == @(${2}*) ]]; then

		nrow=$(($(tail -1 ${1}/$file | cut -f1)+1))  # number of row (number of abstracts) is the greatest row index + 1
		outfolder=${4}/$file.svd

		echo ${1}/$file
		echo $outfolder
		echo $nrow
		echo

		mkdir $outfolder
		sh svd_munin.sh ${1}/$file ${3} $nrow $outfolder > $outfolder/out.${3}.log

	fi
done

# The svd.sh requires these parameters in order:
# {1} target matrix file
# {2} # singular values
# {3} # rows
# {4} output folder
