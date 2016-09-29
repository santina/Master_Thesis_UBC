#!/bin/bash

# Convert ID-termfreq files into Graphlab input matrices

# Call this script with these parameters in order:
# {1} folder with all the ID-termfreq file
# {2} outfolder name

# Usage: sh convert_format.sh input_dir

for FILE in $(ls $1/*)
do
	PREFIX=$(basename $FILE)
	#NUM=$(echo $PREFIX | perl -pe "s/random_pmids_(\d+)/\1/")
	echo $FILE
	echo $PREFIX

	#binaryOut=${2}/term_binary/$NUM.binary.matrix
	matrixFile=${2}/$PREFIX.matrix

	python /projects/slin_prj/slin_prj_results/Master_Thesis_UBC/Shared/Python_Code/convert_format.py --t $FILE --m $matrixFile #--mb $binaryOut



done
