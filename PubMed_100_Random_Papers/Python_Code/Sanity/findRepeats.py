
# Find, if any, repeated abstracts (pubmed IDs) of the training data 

import argparse 
from os import listdir
from os.path import isfile, isdir, join
from collections import defaultdict 


def writeToFile(repeats_list, outfile):
	''' Record the repeated abstracts and the categories they appear in into an outfile 
	'''

	out = open(outfile, 'w')
	for key, categories in repeats_list:
		categories = ' '.join(categories)
		outstring = '\t'.join([str(key), categories])
		out.write(outstring + '\n')
	out.close()

def getRepeats(abstract_docs_dict):
	''' Find repeated abstract (those occurred in more than one category) by 
	picking out the key-value pair for which value (a list) has >1 length 
	'''

	repeats = []
	for key in abstract_docs_dict.keys():
		if len(abstract_docs_dict[key]) > 1:
			repeats.append( (key, abstract_docs_dict[key]) )  # append a tuple 

	return repeats

def buildHash(abstractFolder):
	''' Build a pubmedId: list of categories hash from all the abstract files 
	'''
	
	# Dictionary to keep track of which abstracts are in which category 
	abstract_docs_dict = defaultdict(list)

	for abstractfile in [f for f in listdir(abstractFolder) if isfile(join(abstractFolder, f))]:
		curFile = join(abstractFolder, abstractfile)
		
		# Open the file and write the needed content to the outfile object 
		with open(curFile) as f:
			for line in f:
				line = line.strip().split('\t')
				ID   = int(line[0])  # First item is the PubMed ID of the abstract 
				abstract_docs_dict[ID].append(abstractfile) # filename is the category name

	return abstract_docs_dict



def main():
	parser = argparse.ArgumentParser(description="Check whether there are repeated Pubmed IDs")
	parser.add_argument('--f', type=str, help="folder to all the abstract files")
	parser.add_argument('--out', type=str, help="Write repeated PubMed IDs to this outfile")
	args = parser.parse_args()

	abstract_docs_dict = buildHash(args.f)  # Build a hash 
	repeatedIDs = getRepeats(abstract_docs_dict) # Use a hash to find the repeated abstracts 
	
	if repeatedIDs:
		print "There are repeats"  
		writeToFile(repeatedIDs, args.out)  # Record the PubMed IDs of the repeated abstracts 
	else: 
		print "No repeats"


if __name__ == '__main__':
	main()