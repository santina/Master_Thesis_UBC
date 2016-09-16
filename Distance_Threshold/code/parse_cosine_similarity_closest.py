# See the distances of the Pubmed-recommended papers for plotting 
# for comparison with the distances of all papers in the dataset 

import argparse
import sys
from os import listdir
from os.path import isfile, isdir, join, splitext
import re
import parse_cosine_similarity as ps
import numpy as np


def makeTargetIDSet(idfile):
	IDset = set()
	with open(idfile, 'r') as f:
		for line in f:
			IDset.append(line.split()[0])
	return IDset

def buildClosestPapersHash(answer_file):
	''' Build and return a dictionary that maps target paper ID (key, as a string) to 
	a list of closest papers IDs (strings)
	'''
	h = {}
	with open(answer_file) as f:
		for line in f:
			line = line.strip().split()
			h[line[0]] = line 
	return h

def buildRowtoIDHash(metadata):
	''' Build a row number to PubMed ID hash in order to map row number of matrix pubMed IDs.
	''' 	
	h = {}

	with open(metadata) as f: # PubMed category (target PubMed ID)  PubMedID  title  abstract 
		for lineNum, line in enumerate(f):
			line = line.split('\t')
			h[lineNum] = line[1] # integer key to string value 
	return h

def getsubset(rowNum, line, RowToIDHash, closestPaperIDsHash):
	pairs = line.strip().rstrip(",").split()[-1].split(",")
	wanted_paper_IDs = closestPaperIDsHash[ RowToIDHash[rowNum] ]
	retrieved = []
	subset_distances = []
	for p in pairs: 
		p = p.strip(']').split('[') 
		paperID = RowToIDHash[int(p[1])]
		if paperID in wanted_paper_IDs:
			subset_distances.append(p[0])
			retrieved.append(paperID)

	return subset_distances

def writeDistanceResult(rowNum, line, RowToIDHash, closestPaperIDsHash, out):

	result = getsubset(rowNum, line, RowToIDHash, closestPaperIDsHash)
	
	# Won't be the same because not all closest papers were succesfully retreived (or have abstract)
	# print len(result), len(closestPaperIDsHash[ RowToIDHash[rowNum] ])
	
	# Can't do this assertion because an abstract can appear more than once in a dataset
	# assert len(result) == len(closestPaperIDsHash[ RowToIDHash[rowNum] ])
	out.write(str(rowNum) + ' ' + ' '.join(result) + '\n')


def getClosestDistances(idfile, metafile, distancefile, outfile):
	closestPaperIDsHash = buildClosestPapersHash(idfile)
	RowSet = ps.makeRowSet(closestPaperIDsHash, metafile) # Row numbers of the target papers 
	RowToIDHash = buildRowtoIDHash(metafile)

	out = open(outfile, 'w')
	with open(distancefile, 'r') as f:
		for line in f:
			rowNum = ps.getRowNum(line)
			if rowNum in RowSet:
				writeDistanceResult(rowNum, line, RowToIDHash, closestPaperIDsHash, out)


def main():
	parser = argparse.ArgumentParser(description="parsing out the distances for examination and R input")
	parser.add_argument('--f', type=str, help='a concatenated distance file')
	parser.add_argument('--ids', type=str, help="a file with a list of random IDs and closest IDs")
	parser.add_argument('--meta', type=str, help="the meta file with ids and text")
	parser.add_argument('--o', type=str, help='Out file to write the results to')
	args = parser.parse_args()
	# Each row in the outfile:  ID \t distance1 distance2 distance3 ... 

	#/projects/slin_prj/PubMed_Experiment/random_100_pubmed/data/closestPaperIDs.txt

	getClosestDistances(args.ids, args.meta, args.f, args.o)



if __name__ == '__main__':
	main()