#!/bin/bash
set -e
set -x
target=/projects/bioracle/ncbiData/2015

#curl -O -u anonymous:jlever@bcgsc.ca $root/file_list.txt
#while read
#tail -n +2 file_list.txt | cut -f 1,2 -d '/' | sort | uniq
#curl -O -u anonymous:jlever@bcgsc.ca $root/06/d3/*

# Refer to http://www.nlm.nih.gov/bsd/licensee/access/medline_pubmed.html
mkdir -p $target/medline
cd $target/medline
wget --no-verbose --no-parent --recursive --level=1 --no-directories --user=anonymous --password=jlever@bcgsc.ca ftp://ftp.nlm.nih.gov/nlmdata/.medleasebaseline/gz/

# Refer to http://www.ncbi.nlm.nih.gov/pmc/tools/ftp/
mkdir -p $target/pmc
cd $target/pmc
curl -O -u anonymous:jlever@bcgsc.ca ftp://ftp.ncbi.nlm.nih.gov/pub/pmc/articles.A-B.tar.gz
curl -O -u anonymous:jlever@bcgsc.ca ftp://ftp.ncbi.nlm.nih.gov/pub/pmc/articles.C-H.tar.gz
curl -O -u anonymous:jlever@bcgsc.ca ftp://ftp.ncbi.nlm.nih.gov/pub/pmc/articles.I-N.tar.gz
curl -O -u anonymous:jlever@bcgsc.ca ftp://ftp.ncbi.nlm.nih.gov/pub/pmc/articles.O-Z.tar.gz

