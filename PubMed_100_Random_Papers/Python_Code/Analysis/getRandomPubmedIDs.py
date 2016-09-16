import argparse 
import random
import timeit

def readIDs(filename):
	''' Read in the metadata file to make a list of PubMed IDs
	'''
	IDs = []
	with open(filename) as f:
		for linNum, line in enumerate(f):
			if linNum == 0:
				continue 
			line = line.split('\t')
			pmid = line[2]
			if pmid != "-1": 
				IDs.append(pmid)
	return IDs


def getRandomIDs(numRandomIDs, idlist):
	''' Pull a `numRandomIDs` of pubmedIDs from the list `idList`
	'''
	
	# Check if sample is larger than popoulation:
	if numRandomIDs <= len(idlist):
		randomIndices = random.sample(xrange(len(idlist)), numRandomIDs)
		return [idlist[i] for i in randomIndices ]
	else: 
		return idlist

def writeToFile(outfile, IDs):
	with open(outfile, 'w') as out: 
		for i in IDs:
			out.write(i + '\n')
	

def main():
	parser = argparse.ArgumentParser(description='Get a number of random pubmed IDs and save that to a file')
	parser.add_argument('--meta', type=str, help='Path to the meta where random pubmed IDs will be selected')
	parser.add_argument('--n', type=int, help='Number of random IDs')
	parser.add_argument('--out', type=str, help='Outfolder to which the IDs will be written to')
	parser.add_argument('--nsample', type=int, default=1, help="How many samples of random IDs")
	args = parser.parse_args()

	# Obtain a list of IDs to sample from 
	pmids = readIDs(args.meta)

	for i in range(0, args.nsample):
		outfile = args.out + '/' + 'random_pmids_' + str(i)
		randomIDs = getRandomIDs(args.n, pmids)
		writeToFile(outfile, randomIDs)

	
if __name__ == '__main__':

	t = timeit.default_timer()
	main()
	print "Getting random PuMed IDs took ", str(timeit.default_timer() - t), " seconds"	
