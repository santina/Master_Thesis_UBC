# This is likely to be a one-time use script 
# Reformat /projects/slin_prj/PubMed_Experiment/shallow_vs_deep/data_random_papers/random_abstracts_2821321.txt 
# by getting rid of year and insert a random number in the first column so that the format will fit 
# /projects/slin_prj/slin_prj_results/PubMed_Experiment/random_100_pubmed/code/find_closest_papers.py --meta 
# after concatenating with /projects/slin_prj/PubMed_Experiment/random_100_pubmed/data/abstracts.txt

import argparse

def reformat(line):
	line = line.split('\t')
	
	# Insert a number to indicate that it's a random
	# Remove year, which is the second element 
	line = '\t'.join(['0', line[0], line[2], line[3]])

	return line 


def main():
	parser = argparse.ArgumentParser(description='')
	parser.add_argument('--a', type=str, help='abstract file to be reformatted')
	parser.add_argument('--o', type=str, help='outfile')
	args = parser.parse_args()	

	out = open(args.o, 'w')

	with open(args.a) as f:
		for line in f:
			out.write(reformat(line))
			reformat(line)

	out.close()




if __name__ == '__main__':
	main()

