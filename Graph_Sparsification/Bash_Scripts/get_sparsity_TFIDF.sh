#!/bin/bash

# Obtain the number of entries in the matrix

# Call this script with these parameters in order:
# {1} folder with all the .matrix files

# Usage: sh convert_format.sh input_dir
# Make sure to pipe the result into a file if you want to save the result

H1="matrix_name"
H2="scalar"
H3="sample_rate"
H4="n_entries"

# create a header, -e to enable special characters
echo -e "$H1\t$H2\t$H3\t$H4"

for FILE in $(ls $1)
do

  MATRIX_NAME=$(echo $FILE | cut -d '.' -f1)  # Get the matrix id from folder name
  SCALAR=$(echo $FILE | cut -d '_' -f2)
  RATE=$(echo $FILE | cut -d '_' -f3)
  NENTRIES=$(wc -l $1/$FILE | cut -d ' ' -f1)  # Get the number of entries in the matrix
  echo -e "$MATRIX_NAME\t$SCALAR\t$RATE\t$NENTRIES"

done
