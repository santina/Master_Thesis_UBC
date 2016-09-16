import argparse 
from os import listdir
from os.path import isfile, join
from sets import Set
from collections import defaultdict

# Two fail conditions :
## 1. The entire Efetch record is missing, ie the file that should have all the abstracts for that
## target ID is not there 
## 2. The file doesn't contain all the abstracts, ie there are more related IDs than the abstracts 
## retrieved from Entrez.Bio 


def buildRelatedIDHash(id_file):
	''' Make a dictionary making target ID to a list of most related IDs (including itself)
	'''
	h = defaultdict(list)
	with open(id_file) as f:
		for line in f:
			line = line.strip().split()
			h[line[0]] = line
	return h

def buildIDList(id_file):
	''' Make a list of all the randomly chosen 100 ids ''' 
	idlist = []
	with open(id_file) as f:
		for line in f:
			line = line.strip().split()
			idlist.append(line[0])
	return idlist

def getFileList(abstractFolder):
	''' Make a list of files in the abstractFile '''
	return [f for f in listdir(abstractFolder) if isfile(join(abstractFolder, f))]

def findFailedEfetch(randomIDs, abstractFolder):
	''' Check Fail condition 1 by 
		matching the abstracts files in the abstractFolder to the IDs in relatedIDHash 
	'''
	files = getFileList(abstractFolder)
	missedFiles = []
	for ID in randomIDs:
		if ID not in files:
			missedFiles.append(ID)
	return missedFiles 


	
def main():
	parser = argparse.ArgumentParser(description='')
	parser.add_argument('--f', type=str, help='file with all the ids')
	parser.add_argument('--abstracts', type=str, help='folder with all the abstracts')
	parser.add_argument('--out', type=str, help='outfile to write the report to')
	args = parser.parse_args()
	
	# Check for fail condition 1 
	randomIDs = buildIDList(args.f)
	missedFiles = findFailedEfetch(randomIDs, args.abstracts)
	
	# Check for fail condition 2 
	relatedIDs = buildRelatedIDHash(args.f)


	# Write result to a outfile 
	

if __name__ == '__main__':
	main()