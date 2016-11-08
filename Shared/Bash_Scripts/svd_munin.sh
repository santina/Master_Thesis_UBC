#!/bin/bash

# inputs in this order:
# {1} target matrix file
# {2} # singular values
# {3} # rows
# {4} output folder

# other parameters:
NCPUS=16  # number of cpus you want to use. never more than num-of-cores - 2.
COLS=1062805 # number of columns (size of our wordlist )  #969690 for the newer wordlist 1062805 is a older one
NV=$((${2}+200))	# 200 more than $NSV (extra buffer needed for convergence accuracy)
MAXITER=5

OUT=${4}/out.${2}

echo "doing: ${1}"
echo "output: $OUT"
echo "$HOSTNAME [$(date)]"
GRAPHLAB=/projects/edcc_prj2/sita/bin/GraphLab_22Apr2014/graphlab/release/toolkits/collaborative_filtering #munin and hugin
#GRAPHLAB=/projects/slin_prj/GraphLab_new/PowerGraph/release/toolkits/collaborative_filtering  #gphost03
echo "$GRAPHLAB/svd ${1} --ncpus=$NCPUS --rows=${3} --cols=$COLS --nsv=${2} --nv=$NV --max_iter=5 --quiet=1 --save_vectors=1 --predictions=$OUT"
GRAPHLAB_CMD="$GRAPHLAB/svd ${1} --ncpus=$NCPUS --rows=${3} --cols=$COLS --nsv=${2} --nv=$NV --max_iter=$MAXITER --quiet=1 --save_vectors=1 --predictions=$OUT"
echo "working dir: $(pwd)"
echo $GRAPHLAB_CMD
eval "$GRAPHLAB_CMD"
echo "return: GRAPHLAB:$?"
# check return status at the end
echo "$HOSTNAME [$(date)]"

# Get rid of the files I don't need
rm ${4}/out.${2}.V.1_of_1 ${4}/out.${2}.1_of_1
