# Select a given number of pmids from a file written by "get_midline_pmids.py"

import argparse    # parsing command line args 
import random




def selectIDs(pmidFile, nids):
	id_list = []
	with open(pmidFile) as f:
		for line in f:
			ids = line.strip().split()
			for pmid in ids:
				if random.random() < 0.3:  # to avoid memory issue
					id_list.append(pmid)
	print len(id_list)

	return random.sample(id_list, nids)

def writeIDs(selectedIDs, outfile): 
	with open(outfile, 'w') as out:
		outString = '\n'.join(selectedIDs) + '\n'
		out.write(outString)

def main():
	parser = argparse.ArgumentParser(description='Select a number of pmids')
	parser.add_argument('--f', type=str, help='file that has all the medline pmids')
	parser.add_argument('--n', type=int, help="number of pmids")
	parser.add_argument('--out', type=str, help='file to write all the pmids to')
	args = parser.parse_args()

	selectedIDs = selectIDs(args.f, args.n)
	writeIDs(selectedIDs, args.out)


if __name__ == '__main__':
	main()