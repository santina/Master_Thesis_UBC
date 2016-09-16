#!/bin/bash 

# Convert ID-termfreq files into Graphlab input matrices  

# Call this script with these parameters in order: 
# {1} folder with all the ID-termfreq file
# {2} outfolder name

# Usage: sh convert_format.sh input_dir

for FILE in $(ls $1/*.neighbors.all.tf)
do 
	PREFIX=$(basename $FILE .neighbors.all.tf)
	NUM=$(echo $PREFIX | perl -pe "s/random_pmids_(\d+)/\1/")

	
	binaryOut=${2}/term_binary/$NUM.binary.matrix
	frequencyOut=${2}/term_freq/$NUM.terfreq.matrix

	python ../code/convert_format.py --t $FILE --m $frequencyOut --mb $binaryOut



done