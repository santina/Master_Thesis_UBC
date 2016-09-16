# Remove duplicated IDs in the 1st of closest neighbors of the randomly selected target IDs 
# each file:  PMID Title AbstractText 

import argparse 
from sets import Set
from Bio import Entrez
import time

def removeDuplicate(IDs):
	idHash = Set([]) 
	keptIDs = [] 

	for ID in IDs:
		if ID not in idHash:
			idHash.add(ID)
			keptIDs.append(ID)

	idHash = None  # Not sure if I need to do this for memory 
	return keptIDs 

def entrezCall(pmid):
	for i in range(0, 2): # will retry twice if fail 
		try: 
			handle = Entrez.elink(dbfrom='pubmed', db='pubmed', id=pmid)
			related_info = Entrez.read(handle)
			return related_info
		except : # In case of connection reset by peer or other socket problem
			time.sleep(2) # wait a few seconds before retrying 
			continue 

def writeToFile(outFileObject, IDs):
	IDs = removeDuplicate(IDs)
	outFileObject.write(' '.join(IDs) + '\n')

def writeClosestIDs(IDFile, outfile):
	''' Read each line, which is a ID, and obtain the IDs of its related papers
	'''
	# Set my email 

	with open(IDFile) as f, open(outfile, 'w') as out:
		for lineNum, line in enumerate(f):
			line = line.strip().split()
			ids = []  # will contain closest neighbors to all the closest neighbors of one target ID 
			for pmid in line[1:]: # skip the first pmid since that's the target 

				related_info = entrezCall(pmid)
				related_IDs = related_info[0]['LinkSetDb'][0]['Link']

				for ID in related_IDs:
					ids.append(ID["Id"])

				time.sleep(0.5)  # pause before the next api call 

			writeToFile(out, ids)
			print "Currently at line ", lineNum  # debug, check progress

def main():
	parser = argparse.ArgumentParser(description='')
	parser.add_argument('--f', type=str, help='ID file')
	parser.add_argument('--email', type=str, help="Email for Entrez")
	parser.add_argument('--out', type=str, help='ID file to write to')

	args = parser.parse_args()
	
	Entrez.email = args.email

	writeClosestIDs(args.f, args.out)
	


if __name__ == '__main__':
	main()