# one time use code
# Generate the answer keys from the list of IDs for /projects/slin_prj/slin_prj_results/PubMed_Experiment/random_100_pubmed/code/evaluate_recall.py --a


import argparse

def reformat(targetFile, idsFile, outFile):

	out = open(outFile, 'w')
	targets = open(targetFile, 'r').readlines()

	with open(idsFile) as f:
		for lineNum, ids in enumerate(f): 
			target = targets[lineNum].split()[0]
			out.write(target + ' ' + ids)


	out.close()

def combine(targetFile, idsFile, outFile):
	out = open(outFile, "w")
	targets = open(targetFile, 'r').readlines()

	with open(idsFile) as f:
		for lineNum, ids in enumerate(f): 
			target = targets[lineNum].strip()
			out.write(target + ' ' + ids)

	out.close()

def main():
	parser = argparse.ArgumentParser(description='')
	parser.add_argument('--a', type=str, help='contain target ID as the first item in each line')
	parser.add_argument('--a2', type=str, help="the files with all the IDs but no target ID")
	parser.add_argument('--o', type=str, help='outfile')
	args = parser.parse_args()	

	
	combine(args.a, args.a2, args.o)

if __name__ == '__main__':
	main()