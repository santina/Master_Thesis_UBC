#!/bin/bash

# Convert ID-termfreq files into Graphlab input tf_idf matrices

# Call this script with these parameters in order:
# {1} folder with all the ID-termfreq file
# {2} root outfolder name to store the files

# Usage: sh convert_format.sh input_dir

for FILE in $(ls $1/*)
do
	PREFIX=$(basename $FILE)

	tfidfOut=${2}/$PREFIX.tfidf

	python ../Python_Code/tf_idf.py --t $FILE --tfidf $tfidfOut

done
