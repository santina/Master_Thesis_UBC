#!/bin/bash 

# Convert ID-termfreq files into Graphlab input tf_idf matrices  

# Call this script with these parameters in order: 
# {1} folder with all the ID-termfreq file
# {2} root outfolder name to store the files

# Usage: sh convert_format.sh input_dir

for FILE in $(ls $1/*.neighbors.all.tf)
do 
	PREFIX=$(basename $FILE .neighbors.all.tf)
	NUM=$(echo $PREFIX | perl -pe "s/random_pmids_(\d+)/\1/")

	tfidfOut=${2}/original_files_tfidf/$NUM.tf_idf
	matrixFile=${2}/tf_idf/$NUM.tf_idf.matrix

	# maybe do mkdir in case the folders aren't yet exist

	python ../code/tf_idf.py --t $FILE --tfidf $tfidfOut
	python ../code/convert_format.py --t $tfidfOut --m $matrixFile
done