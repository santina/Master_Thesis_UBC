import argparse
import sys
from os import listdir
from os.path import isfile, isdir, join, splitext
import re

def makeset(idfile):
	idset = set()
	with open(idfile, 'r') as f:
		for line in f:
			idset.add(line.strip())

	print len(idset)
	return idset 

def makeRowSet(IDset, metafile):
	rowNumSet = set()

	with open(metafile, 'r') as f:
		for linNum, line in enumerate(f): 
			paperID = line.split()[1]
			if paperID in IDset: 
				rowNumSet.add(linNum)

	print len(rowNumSet)
	return rowNumSet

def getRowNum(line):
	assert "TRACKING" in line
	return int(re.findall(r'\[(\d+)\]', line)[0])

def findClosetPapersResult(line, out):
	rowIDs = re.findall(r'\[(\d+)\]', line)
	return rowIDs 

def writeDistancesResult(rowNum, line, out, tol=0.00000000001):
	# Matching number that follows a tab or a comma 
	words = line.strip().rstrip(",").split()[-1].split(",")
	words2 = [w.split("[")[0] for w in words]
	wordsF = [float(w) for w in words2]
	#assert len(wordsF) == dim
	assert max(wordsF) < 1 + tol and min(wordsF) > -1 - tol
	out.write(str(rowNum) + ' ' + ' '.join(words2) + '\n')


def getNeededDistances(idfile, metafile, distancefile, outfile):
	IDset = makeset(idfile)
	RowSet = makeRowSet(IDset, metafile)

	out = open(outfile, 'w')
	with open(distancefile, 'r') as f:
		for line in f:
			rowNum = getRowNum(line)
			if rowNum in RowSet:
				writeDistancesResult(rowNum, line, out)


def main():
	parser = argparse.ArgumentParser(description="parsing out the distances for examination and R input")
	parser.add_argument('--f', type=str, help='a concatenated distance file')
	parser.add_argument('--ids', type=str, help="a file with a list of random IDs")
	parser.add_argument('--meta', type=str, help="the meta file with ids and text")
	parser.add_argument('--o', type=str, help='Out file to write the results to')
	args = parser.parse_args()
	# Each row in the outfile:  ID \t distance1 distance2 distance3 ... 

	# makeset(args.ids)  #/projects/slin_prj/PubMed_Experiment/random_100_pubmed/data/random_PubMedIDs.txt

	getNeededDistances(args.ids, args.meta, args.f, args.o)



if __name__ == '__main__':
	main()