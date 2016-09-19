#!/bin/bash
set -e -x

git clone https://github.com/dato-code/PowerGraph.git

cd PowerGraph

# Apply fix to use latest version of libevent (as previous download file is missing) (and the appropriate hash for the file)
perl -pi -e 's|http://iweb.dl.sourceforge.net/project/levent/libevent/libevent-2.0/libevent-2.0.18-stable.tar.gz|http://downloads.sourceforge.net/project/levent/release-2.0.22-stable/libevent-2.0.22-stable.tar.gz|g' CMakeLists.txt
perl -pi -e 's|aa1ce9bc0dee7b8084f6855765f2c86a|c4c56f986aa985677ca1db89630a2e11|g' CMakeLists.txt

# Apply fix so that  machines with >64 cores can execute Powergraph
perl -pi -e 's/typedef fixed_dense_bitset<64> affinity_type;/typedef fixed_dense_bitset<128> affinity_type;/' src/graphlab/parallel/fiber_control.hpp

# Let's configure the project
./configure --no_mpi --no_jvm

# And then build the collaborative filtering library specifically
cd release/toolkits/collaborative_filtering/
make

