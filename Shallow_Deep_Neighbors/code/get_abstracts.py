# Get closest paper IDs 
import argparse 
import time
from Bio import Entrez
import random as rd


# TODO: think if we need to account for review or papers in general 

def getAbstracts(ids, results, omittedIDs):
	idString = ' '.join(ids)
	papers = None 

	for i in range(0, 2): # Only gonna retry twice 
		try: 
			handle = Entrez.efetch(db="pubmed", id=idString, rettype="abstract")
			papers = Entrez.read(handle)
		except : # In case of connection reset by peer or other socket problem
			time.sleep(3) # wait a few seconds before retrying 
			continue 
		if papers: # if succesffully retrieve the papers, break out the loop
			break

	if papers: # If successfully retreived papers text 
		index = 0  # Keep track of which pmids in the array `ids`
		
		for paper in papers: 
			try: 
				title =  paper["MedlineCitation"]["Article"]["ArticleTitle"]
			except KeyError:
				title = ""
			try: 
				abstract =  ' '.join(paper["MedlineCitation"]["Article"]["Abstract"]["AbstractText"])
			except KeyError:
				abstract = ""

			if title and abstract: # only if we have all information 
				results.append((ids[index], title, abstract))
			else: 
				omittedIDs.append(ids[index])

			index += 1 

			handle.close()
	else: 
		pass 
		# We don't care if we're missing 100 out of 3 millions or so papers but still nice to know 
		# how many were omitted 


def getAllAbstracts(pmids):
	''' Take a string of pmids and get the title, journal name, and the abstract for all of them. 
	Also return a list of IDs of omitted papers 
	'''

	omitted = []
	results = []

	# Breakdown the pmids to groups of 100 to avoid HTTP error 414: request URI too long 

	pmids = pmids.split()
	targetID = pmids[0]
	seg_length = 150
	pmids_segs = [pmids[x:x+seg_length] for x in range(0,len(pmids),seg_length)]

	for ids in pmids_segs:
		getAbstracts(ids, results, omitted)

		# Wait for 2 to 6 seconds before the next API call 
		sleeptime = rd.randrange(2, 6) 
		time.sleep(sleeptime)
		
	return results, omitted


def writeToFile(results, outFileObject):
	''' Write the result to a file handler 
	'''
	for paper in results:
		try: 
			outFileObject.write('\t'.join([info for info in paper]) + '\n')  
		except UnicodeEncodeError: 
			outFileObject.write('\t'.join([info.encode('ascii', 'ignore') for info in paper]) + '\n') 
			

def writeAbstractsFiles(IDfile, outFile, logfile):
	''' Retrieve abstract text for each pubmed ID
	in the given an file (`IDfile`) with all the IDs
	and write the abstracts to the outfile and a summary to the log file 
	'''
	with open(IDfile) as f, open(outFile, 'w') as out, open(logfile, 'w') as log: 
		for line in f:

			results, omittedIDs = getAllAbstracts(line.strip())
			# Write to result files 
			writeToFile(results, out)
			# Log the information about each iteration: omitted IDs for those without abstracts 
			log.write(' '.join(omittedIDs) + '\n')


def main():

	parser = argparse.ArgumentParser(description='Get abstracts and save that to files')
	parser.add_argument('--f', type=str, help='file that has all the IDs')
	parser.add_argument('--out', type=str, help='file to write all the abstracts to')
	parser.add_argument('--e', type=str, help="For error logging")
	parser.add_argument('--email', type=str, help="Email for using Entrez.Bio")
	args = parser.parse_args()

	# Set my email 
	Entrez.email = args.email

	# Get closest abstracts for each paper (ID)
	writeAbstractsFiles(args.f, args.out, args.e)


if __name__ == '__main__':
	main()
