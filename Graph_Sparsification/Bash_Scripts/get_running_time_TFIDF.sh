#!/bin/bash

# Get running time of SVDs on the tfidf matrices in the graph sparsification experiment

# Call this script with these parameters in order:
# {1} folder with all the SVD output folders

# Usage: sh convert_format.sh input_dir
# Make sure to pipe the result into a file if you want to save the result

H1="matrix_name"
H2="scalar"
H3="sample_rate"
H4="run_time"

# create a header, -e to enable special characters
echo -e "$H1\t$H2\t$H3\t$H4"

for FOLDER in $(ls $1)
do
  for LOG in $(ls $1/$FOLDER/*.log)
  do
    MATRIX_NAME=$(echo $FOLDER | cut -d '.' -f1)  # Get the matrix id from folder name
    SCALAR=$(echo $FOLDER | cut -d '_' -f2)
    RATE=$(echo $FOLDER | cut -d '_' -f3)
    TIME=$(grep "Final Runtime (seconds):" $LOG | grep -o "[0-9.]*")  # Get the running seconds
    echo -e "$MATRIX_NAME\t$SCALAR\t$RATE\t$TIME"
  done
done
