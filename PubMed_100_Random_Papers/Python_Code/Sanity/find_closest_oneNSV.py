# Find the closest papers to each of the 100 random PubMed IDs given a number of singular value
# Also record the distance to sanity check the sorting

import numpy as np
import timeit
import heapq
import argparse 
from scipy.spatial.distance import euclidean 
from scipy.spatial.distance import cosine 
import math
from collections import defaultdict 

def countLine(filename):
	count = 0
	with open(filename) as f:
		for lineNum, line in enumerate(f): # 0 base for lineNum 
			count = lineNum + 1
	return count 

def buildPaperHash(metadata):
	''' Build a row number to PubMed ID hash in order to map row number of matrix pubMed IDs.
	''' 	
	row_to_ID = {}
	ID_to_row = {}

	with open(metadata) as f: # PubMed category (target PubMed ID)  PubMedID  title  abstract 
		for lineNum, line in enumerate(f):
			line = line.split('\t')
			row_to_ID[lineNum] = line[1] # integer key to string value 
			ID_to_row[line[1]] = lineNum # string key to integer value
	return row_to_ID, ID_to_row

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

def readMatrix(filename, nrow, numSV): 
	''' Read in decomposed matrices U or V 	
	'''
	matrixU = np.zeros((nrow, numSV)) 

	with open(filename, "rb") as f:
		for line in f: 
			line = line.split()
			# x[0] is index and the rest are values
			matrixU[int(line[0])] = [float(num) for num in line[1:numSV+1]] 
	return matrixU

def getSVals(filename, numSV, header=True):
	''' Read in a given number of singular values 
	'''
	singularVals = []

	with open(filename) as f:
		for index, line in enumerate(f): # 0 base for lineNum 
			if header and index == 0: 
				continue 
			elif index > numSV: # If has recorded the desired number of values
				break
			else: 
				singularVals.append(float(line))
	return singularVals

def scaleMatrix(matrix, singularVals):
	''' Scale the matrix by square root such m_ij = sqrt(s_j)*m_ij
	for later's distance calculation to be sum(s_0*(a_0-b_0)^2 + s_1*(a_1-b_1)^2,...) 
	''' 
	#matrix = np.multiply(matrix, np.sqrt(singularVals))
	matrix = np.multiply(matrix, singularVals)
	return matrix

def normalizeMatrix(matrix, ncols=None):
	''' Calculate normalization of a part of `matrix`. Store
	and return that as a new matrix 
	'''
	rowNum = 0
	if not ncols: # default to normalize the whole matrix
		ncols = matrix.shape[1] 
	newMatrix = np.zeros((matrix.shape[0], ncols))
	
	for row in matrix:
		norm = np.linalg.norm(row[:ncols])
		# if norm is not 0, i.e. the row isn't all zeros
		if norm: 
			newMatrix[rowNum] = [number/norm for number in row[:ncols]]
		rowNum += 1

	return newMatrix


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


def writeResults_dist_index(closetPapersH, ID_to_row, matrix, nsv, outfile):
	with open(outfile, "w") as out:
		for targetPmid in closetPapersH.keys():
			try: 
				targetIndex = ID_to_row[targetPmid]
			except KeyError: # meaning this targetPmid isn't in the abstract file because it has no abstract
				continue  # skip it 
			result = findClosestRows(matrix, targetIndex, len(closetPapersH[targetPmid]), cosine)
			resultString = str(targetIndex) + ' '
			for pair in result:
				resultString += str(pair[0]) + '[' + str(pair[1]) + ']' + ' '
			
			out.write(resultString + '\n')

def main():  
	parser = argparse.ArgumentParser(description="Find closest papers")
	parser.add_argument('--m', type=str, help="Path to the decomposed matrix")
	parser.add_argument('--s', type=str, help="Path to the singular values file")
	parser.add_argument('--a', type=str, help="Path to the list of abstracts that made the matrix")
	parser.add_argument('--out', type=str, help="Folder to write the file to")
	parser.add_argument('--nsv', type=int, help="Number of singular values to look at")

	args = parser.parse_args()

	nrow = countLine(args.a)
	print nrow
	# Make matrix and singular value array 
	matrix = readMatrix(args.m, nrow, args.nsv)
	svals = getSVals(args.s, args.nsv)
	matrix = normalizeMatrix(scaleMatrix(matrix, svals))

	# Obtain a list and hashes to control our calculation 
	row_to_ID, ID_to_row = buildPaperHash(args.a)	 	  # a hash of row number (integer) to PubMed ID (string)
	closetPapersH = buildClosestPapersHash(args.a) 

	t = timeit.default_timer()
	writeResults_dist_index(closetPapersH, ID_to_row, matrix, args.nsv, args.out)

	print timeit.default_timer() - t


if __name__ == '__main__':
	main()