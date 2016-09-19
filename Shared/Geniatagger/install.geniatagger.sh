#!/bin/bash

# First let's install GeniaTagger

wget http://www.nactem.ac.uk/tsujii/GENIA/tagger/geniatagger-3.0.1.tar.gz

tar xvf geniatagger-3.0.1.tar.gz

cd geniatagger-3.0.1

# Fix a missing header
echo "#include <cstdlib>" > morph2.cpp
cat morph.cpp >> morph2.cpp
mv morph2.cpp morph.cpp

make

cd -

rm geniatagger-3.0.1.tar.gz

# Then let's install a Python wrapper for it
pip install geniatagger-python

