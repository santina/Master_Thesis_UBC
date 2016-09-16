# Extract the corresponding line from from a file in a folder of abstract files given 
# a list of pmids 

import argparse    # parsing command line args 
import random
import os, os.path # accessing files and folders 
from collections import defaultdict


def getIDs(abstractFile):
	ids = []
	with open(abstractFile) as f:
		for line in f:
			line = line.split()
			ids.append(line[0])
	return ids 

def getSelectedIDs(pmidFile):
	''' The ID file is suppose to have one ID per line ''' 
	ids = []
	with open(pmidFile) as f:
		for line in f:
			ids.append(line.strip())
	return ids

def buildpmidHash(folder):
	files = [f for f in os.listdir(folder) if os.path.isfile(os.path.join(folder, f))]
	fileNameToIDList = defaultdict(list)

	for f in files:
		abstractFile = os.path.join(folder, f)		
		fileNameToIDList[abstractFile] = getIDs(abstractFile)

	return fileNameToIDList

def findFile(fileNameToIDList, pmid):
	abstractFile = ""
	for key in fileNameToIDList:
		if pmid in fileNameToIDList[key]:
			return key 

def findAbstract(abstractFile, pmid):
	with open(abstractFile) as f:
		for line in f:
			if line.split()[0] == pmid:
				return line 

def writeAbstracts(selectedIDs, outfile, fileNameToIDList):

	with open(outfile, 'w') as out:
		for pmid in selectedIDs:
			abstractFile = findFile(fileNameToIDList, pmid)
			abstractInfo = findAbstract(abstractFile, pmid)
			if not abstractInfo:
				print "We have a problem"
			else: 
				out.write(abstractInfo)

def main():
	parser = argparse.ArgumentParser(description='Select a number of pmids')
	parser.add_argument('--f', type=str, help='folder of medline abstracts')
	parser.add_argument('--pmid', type=str, help="the pmids file")
	parser.add_argument('--out', type=str, help='file to write all the abstracts to')
	args = parser.parse_args()

	selectedIDs = getSelectedIDs(args.pmid) # Get the list of pmids from the pmid file 
	fileNameToIDList = buildpmidHash(args.f)
	writeAbstracts(selectedIDs, args.out, fileNameToIDList)


if __name__ == '__main__':
	main()