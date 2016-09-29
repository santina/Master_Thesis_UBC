#!/bin/bash

# sample ID-termfreq files

# Call this script with these parameters in order:
# {1} folder with all the ID-termfreq file
# {2} outfolder name

# Usage: sh convert_format.sh input_dir

for FILE in $(ls $1/*.tf)
do
  for i in `seq 1 9`
  do
    echo $FILE
    # Do some parsing
    PREFIX=$(basename $FILE .neighbors.all.tf)  # basename: a command
    NUM=$(echo $PREFIX | perl -pe "s/random_pmids_(\d+)/\1/")
    Rate=$(echo "scale=1; $i/10.0" | bc)

    for j in `seq 1 3`
    do
    	frequencyOut=${2}/${NUM}.sampled.tf_${Rate}_${j}
      echo $frequencyOut
      python /projects/slin_prj/slin_prj_results/Master_Thesis_UBC/Graph_Sparsification/Code/sample_graph.py \
      --f $FILE --out $frequencyOut --rate $Rate
    done

  done

done
