
''' For finding precisions for a number of Pubmed experiment instance. So this is a combination of
	find_closest_papers.py evalute_recall.py, so to avoid having many intermediate result files.
'''

import find_closest_papers as find
import evaluate_recall as evaluate
import argparse
from os import listdir
from os.path import isfile, isdir, join
import re
from collections import defaultdict
from scipy.spatial.distance import euclidean
from scipy.spatial.distance import cosine
import numpy as np
import timeit
import heapq
import sys

def findClosestRows(matrix, rowNum, nNeighbors, distfunc):
	''' Calculate Euclidean distance of the given row to all other rows in the matrix
		Use a heap invariant to maintain the order and return top `nNeighbors` smallest distances
	'''
	heap = []  # a heapified array of tuple (distance, row_number)
	index = 0
	for row in matrix:

		if distfunc == euclidean:
			dist = distfunc(matrix[rowNum], row)
		elif distfunc == cosine:
			dist = 1 - np.dot(matrix[rowNum], row)

		heapq.heappush(heap, (dist, index))

		index += 1

	return heapq.nsmallest(nNeighbors, heap)


def countLine(filename):
	count = 0
	with open(filename) as f:
		for lineNum, line in enumerate(f): # 0 base for lineNum
			count = lineNum + 1
	return count

def getSVals(logfile, numSV):
	''' Read in a given number of singular values, done rather inefficiently ....
	'''
	singularVals = []

	with open(logfile) as f:
		for line in f: # 0 base for lineNum
			if "Singular value " and "Error estimate:" in line:
				line = line.split()
				singularVals.append(float(line[3]))

	return singularVals[:numSV]

def writeResult(result, outfileObject):
	''' result is a tuple of length 4 : experiment#, distance function, nsv, precision '''
	result_asString = '\t'.join([ str(info) for info in result ])
	outfileObject.write(result_asString + '\n')

def getFilePaths(topFolder, fileExtension=""):
	''' return a list of all files (full paths) in that folder with the given file extension, which could
	be any part of the file, recursively '''
	allfiles = []

	for f in [f for f in listdir(topFolder)]:
		curFile = join(topFolder, f)

		if isdir(curFile):
			files = getFilePaths(curFile, fileExtension)
			for f in files: allfiles.append(f)

		elif isfile(curFile) and fileExtension in curFile:
			allfiles.append(curFile)

	return allfiles

def findFile(filelist, matrixFile, level):
	''' Pull out the file in filelist that corresponds to matrixFile
		Level means where the file name matching should occur, level = 1 means
		matching to the filename with no other folder name, level = 2 means matching to the folder
		immediately above it
	'''
	# Pull out the number
	number = re.findall(r'\d+', matrixFile.split('/')[-2]) # Find the number in the file name (not full path)
	assert len(number) == 1 # should be an array of length 1, ie only finding one number
	experimentNum = number[0]

	for f in filelist:
		number = re.findall(r'\d+', f.split('/')[-level])[0]
		if number == experimentNum:
			return f

def buildPaperHash(answerFile):
	''' Build a row number to PubMed ID hash and another one vice versa in order to map row number of matrix to
		or from pubMed IDs.
	'''
	rowNumToPmid = {}
	pmidToRowNum = {}

	index = 0
	with open(answerFile) as a: # PubMed category (target PubMed ID)  PubMedID  title  abstract
		for answer in a:
			answer = answer.strip().split('\t')
			rowNumToPmid[index] = answer[1] # integer key to string value
			pmidToRowNum[answer[1]] = index # string key to integer value
			index += 1
	return rowNumToPmid, pmidToRowNum

def buildClosestPapersHash(answerFile):
	''' Build and return a dictionary that maps target paper ID (key, as a string) to
		a list of closest papers IDs (strings)
	'''
	h = defaultdict(list)
	with open(answerFile) as f:
		for line in f:
			line = line.strip().split()
			h[line[0]].append(line[1])
	return h

def calculate_precision(matrix, targetRowIndex, true_indices, distfunc, rowNumToPmid):
	''' Measure the recall by seeing how many hits in predictions are in the actual answers
	'''
	localScore = 0

	nNeighbors = len(true_indices)
	rows_info = findClosestRows(matrix, targetRowIndex, nNeighbors, distfunc)  # a list of tuples (dist, index)
	predicted_rows = [pair[1] for pair in rows_info]  # extract out the indices in each tuple

	print [rowNumToPmid[d] for d in predicted_rows]


	assert len(predicted_rows) == len(true_indices)

	# Measure the recall by seeing how many hits in predictions are in the actual answers
	for row_index in predicted_rows:
		if row_index in true_indices:
			localScore += 1

	return float(localScore)/nNeighbors  # return precision

def get_precision(matrix, rowNumToPmid, pmidToRowNum, closestPapers, distfunc):
	''' Get precision for this combination of parameters
	'''

	# time how long this function takes
	time0 = timeit.default_timer()

	# Intialize variables
	totalScore = 0
	totalPapers = 0

	for target in closestPapers.keys():
		try: # Find the row index of the current target paper
			targetRowIndex = pmidToRowNum[target]
		except KeyError: # When the target doesn't have an abstract
			print "Key error for some reason, " , target
			continue

		totalPapers += 1 # Increment the number of papers we are looking at

		# Calculate the precision score for one paper
		true_indices = [pmidToRowNum[ID] for ID in closestPapers[target]] # list of row indices
		totalScore += calculate_precision(matrix, targetRowIndex, true_indices, distfunc, rowNumToPmid)

	# Return elapsed time and the average precision
	return timeit.default_timer() - time0, float(totalScore)/totalPapers

def getAvgPrecision(matrixFile, logFile, answerFile, outfileObject):
	''' Make several necessary data structure to further calculate precision for different nsv
	'''

	# Build a few hashes
	rowNumToPmid, pmidToRowNum = buildPaperHash(answerFile) # integer key to string value
	closestPapers = buildClosestPapersHash(answerFile)

	assert len(rowNumToPmid.keys()) == len(pmidToRowNum.keys())

	# make a numpy matrix from the matrixfile
	matrix = find.readMatrix(matrixFile, countLine(answerFile), 1500)
	svals = getSVals(logFile, 1500)
	matrix = find.scaleMatrix(matrix, svals)

	# Experiment Name (a number):
	experimentNum = re.findall(r'\d+', matrixFile.split('/')[-2])[0]

	nMatrix = find.getMatrixSubset(matrix, 50)
	# t_e, precision_e = get_precision(nMatrix, rowNumToPmid, pmidToRowNum, closestPapers, euclidean)
	# writeResult((experimentNum, "Euclidean", nsv, precision_e, t_e), outfileObject)

	nMatrix = find.normalizeMatrix(nMatrix)
	t_c, precision_c = get_precision(nMatrix, rowNumToPmid, pmidToRowNum, closestPapers, cosine)
	# writeResult((experimentNum, "Cosine", 50, precision_c, t_c), outfileObject)

	print experimentNum, "Cosine"

def getResult(matrixFolder, answersFolder, outfile):

	# get all the files needed for this evaluation
	matrixFiles = getFilePaths(matrixFolder, "U")  # decmposed matrix
	matrixLogs = getFilePaths(matrixFolder, ".log") # singular value
	answerFiles = getFilePaths(answersFolder, ".all") # which paper are close to which ones

	# sanity check
	assert len(matrixFiles) == len(matrixLogs)
	assert len(matrixFiles) == len(answerFiles)

	# open the outfile
	out = open(outfile, 'w')

	# now loop through each triple of files that correspond to each other
	for i in range(0, len(matrixFiles)):
		curMatrix = matrixFiles[i]
		curLog = findFile(matrixLogs, curMatrix, 2)
		curAnswer = findFile(answerFiles, curMatrix, 1)

		assert curMatrix and curLog and curAnswer  # making sure we have all of them
		print curMatrix
		print curLog
		print curAnswer

		getAvgPrecision(curMatrix, curLog, curAnswer, out)


def main():
	parser = argparse.ArgumentParser(description="Evaluating multiple Pubmed experiment instances")
	parser.add_argument('--f', type=str, help='matrix folder to all the instances')
	parser.add_argument('--a', type=str, help='Folder with the answer keys: concatenated abstracts')
	parser.add_argument('--o', type=str, help='Out file to write the results to')
	args = parser.parse_args()

	getResult(args.f, args.a, args.o)

if __name__ == '__main__':
	main()
