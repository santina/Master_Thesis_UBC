#!/bin/bash

# target matrix: 
TARGET=/projects/slin_prj/PubMed_Experiment/matrices/term_freq.matrix

NCPUS=16  # number of cpus you want to use. never more than num-of-cores - 2.  
ROWS=12440 # number of rows
COLS=1062805 # number of columns
NSV=4000 # number of singular values you want
NV=$(($NSV+100))	# 200 more than $NSV (extra buffer needed for convergence accuracy)

MAXITER=5

OUT_DIR=/projects/slin_prj/PubMed_Experiment/GraphLab_SVD_results/term_freq
#mkdir -p $OUT_DIR

OUT=$OUT_DIR/out.$NSV

echo "doing: $TARGET"
echo "output: $OUT"
echo "$HOSTNAME [$(date)]"
GRAPHLAB=/projects/edcc_prj2/sita/bin/GraphLab_22Apr2014/graphlab/release/toolkits/collaborative_filtering
echo "$GRAPHLAB/svd $TARGET --ncpus=$NCPUS --rows=$ROWS --cols=$COLS --nsv=$NSV --nv=$NV --max_iter=5 --quiet=1 --save_vectors=1 --predictions=$OUT"
$GRAPHLAB/svd $TARGET --ncpus=$NCPUS --rows=$ROWS --cols=$COLS --nsv=$NSV --nv=$NV --max_iter=$MAXITER --quiet=1 --save_vectors=1 --predictions=$OUT
echo "return: GRAPHLAB:$?" 
# check return status at the end
echo "$HOSTNAME [$(date)]" 

