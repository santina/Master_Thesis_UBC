# this python script will create the data needed to create the evaluation survey
# by looking at the processed rank analysis file
# The original rank analysis file is created by 'find_ranks.sh' in /projects/slin_prj/PubMed_Experiment/big_matrix/bash_script
# The processed is by sorting by the average rank, and then taking the first 100 lines
# Hence creating the chosen 100 abstracts. ex : sort -k 4 -n 200 > 200.sorted

import sys
import argparse
import random
from Bio import Entrez
import time

def main():
    # Parse the arguments
    args = parseArgs()
    Entrez.email = args.email
    make_survey_data(args.f, args.out)

def parseArgs():
    """ Parse the argument and do sanity check """
    parser = argparse.ArgumentParser(description='Create survey input data' )
    parser.add_argument('--f', type=str, help='rank analysis data')
    parser.add_argument('--email', type=str, help="Email for using Entrez")
    parser.add_argument('--out', type=str, help='Output file')
    args = parser.parse_args()

    return args

def make_survey_data(rank_file, outfile):
    out = open(outfile, "w")

    with open(rank_file) as f:
        for line in f:
            line = line.strip().split('\t')

            # Obtain all the relevant pmids
            target_pmid = line[0].split('-')[0]
            svd_pmid = line[1].split('-')[0]
            pubmed_pmid = get_pubmed_rank1(line)

            # Get the data to write to file
            data = request_data(target_pmid, pubmed_pmid, svd_pmid)

            if data:
                # write to outfile
                out.write(str(data) + '\n')

def get_pubmed_rank1(split_line):
    top10 = eval(split_line[-1])
    top10 = sorted(top10, key=lambda x: x[1])  # sort by the pubmed rank
    return str(top10[0][2])

def request_data(target_pmid, pubmed_pmid, svd_pmid):
    """ Create a JSON object that contains the information for each abstract """
    pmids = ' '.join([target_pmid, pubmed_pmid, svd_pmid])

    for i in range(0, 2): # trying twice
        try:
            handle = Entrez.efetch(db="pubmed", id=pmids, rettype="abstract")
            papers = Entrez.read(handle)
            papers = papers['PubmedArticle']
        except:
            time.sleep(3)
            continue
        if papers:
            break

    if len(papers) == 3:  # Successfully retrieve the information
        return create_data(target_pmid, pubmed_pmid, svd_pmid, papers)

    else:
        print("Unable to retrieve for: " + target_pmid + '\n')
        return None

def create_data(target_pmid, pubmed_pmid, svd_pmid, papers):
    pubmed_choice = random.randrange(1,3)
    svd_choice = 2 if pubmed_choice == 1 else 1

    data = {
        "target" : create_subdata(target_pmid, papers[0], ""),
        "pubmed" : create_subdata(pubmed_pmid, papers[1], pubmed_choice),
        "svd" : create_subdata(svd_pmid, papers[2], svd_choice),
    }
    
    return data

def create_subdata(pmid, paper, choice):
    subdata = {
        "ID" : pmid,
        "title": paper["MedlineCitation"]["Article"]["ArticleTitle"],
        "abstract" :
        ' '.join(paper["MedlineCitation"]["Article"]["Abstract"]["AbstractText"]),
        "choice" : choice
    }
    return subdata


if __name__ == '__main__':
	main()
