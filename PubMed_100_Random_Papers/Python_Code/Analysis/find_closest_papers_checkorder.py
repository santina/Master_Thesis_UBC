# Find the closest papers to each of the 100 random PubMed IDs

import numpy as np
import timeit
import heapq
import argparse 
import sys

def buildPaperHash(metadata):
	''' Build a row number to PubMed ID hash in order to map row number of matrix pubMed IDs.
	''' 	
	h = {}

	with open(metadata) as f: # PubMed category (target PubMed ID)  PubMedID  title  abstract 
		for lineNum, line in enumerate(f):
			line = line.split('\t')
			h[lineNum] = line[1] # integer key to string value 
	return h

def getListOfTargets(file_name):
	''' Get a list of pubMed IDs by looking into the category folders. 
	''' 
	categories = []

	with open(file_name) as f:
		for line in f:
			if line:
				categories.append(line.strip())
	return categories

def buildNumRetrivalsHash(file_name):
	h = {}
	with open(file_name) as f:
		for line in f:
			line = line.split()
			h[line[0]] = int(line[1])
	return h

def readMatrix(filename, nrow, numSV, outfolder): 
	''' Read in decomposed matrices U or V 	
	'''
	matrixU = np.zeros((nrow, numSV)) 
	out = open(outfolder+"/weirdlines.txt", "w")


	
	with open(filename, "rb") as f:
		for lineNum, line in enumerate(f): 
			line = line.strip().split()
			length = len(line) - 1 # Get the number of available sv
			
			# x[0] is index and the rest are values
			# matrixU[int(line[0])] = [float(num) for num in line[1:numSV+1]]
			try: 
				if length >= numSV:
					matrixU[int(line[0])] = [float(num) for num in line[1:numSV+1]]
				else: 
					matrixU[int(line[0])][0:length] = [float(num) for num in line[1:]] # line[1:length+1] 
			except ValueError:
				out.write(str(lineNum) + "\n")
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

def getMatrixSubset(matrix, ncols):
	''' Return a subset of the matrix (first `ncols`)
	'''
	newMatrix = np.zeros((matrix.shape[0], ncols))
	index = 0
	for row in matrix:
		newMatrix[index] = row[:ncols]
		index += 1
	return newMatrix 

def getCosineDistance(vectorA, vectorB):
	''' Calculate and return cosine distance of two **normalized** vectors 
	'''
	return np.dot(vectorA, vectorB)

def getEuclidenDistance(vectorA, vectorB):
	''' Calculate and return Euclidean distance of two vectors: 
	'''
	score = 0
	for i in range(0, len(vectorA)):
		score += (vectorA[i] - vectorB[i])**2 

	return score**0.5 # take the square root 

def findClosestRowsByCosine(matrix, rowNum, nNeighbors, nsv):
	''' Calculate cosine distance of the given row to all other rows in the matrix
	Use a heap invariant to maintain the top `nNeighbors` greatest cosine distances 
	'''
	heap = []  # a heapified array of tuple (distance, row_number)
	index = 0
	for row in matrix:
		dist = np.dot(matrix[rowNum][:nsv], row[:nsv])
		
		# If we haven't found nNeighbors of closestRows 
		# or 'dist' is greater than the smallest recorded distance in `heap`
		# then we need to add `dist` to `heap` 

		if len(heap) < nNeighbors or dist > heap[0][0]:
			
			# If the heap is full,remove the smallest
			if len(heap) == nNeighbors:
				heapq.heappop(heap)

			heapq.heappush(heap, (dist, index))

		index += 1

	return heapq.nlargest(nNeighbors, heap) # return top largest distances in sorted order 



def writeToFile(pubmedID, result, out, paperID_h):
	''' Delimited by a space for each document ID 
	'''
	docIDs = []

	for tuple in result:
		docIDs.append(paperID_h[tuple[1]])
	out.write(pubmedID + '\t' + ' '.join([str(i) for i in docIDs]) +'\n')

def writeCosineResults(matrix, outfile, categories, paperID_h, npapers_h, nsv):
	''' Go through the entire matrix and find closest rows to each row 
	by Cosine distance and write the result to `outfile`
	'''
	with open(outfile, 'w') as out:
		for i in range(0, matrix.shape[0]):
			pubMedID = paperID_h[i]
			if pubMedID in categories:  # Only calculate for the row of the category 
				result = findClosestRowsByCosine(matrix, i, npapers_h[pubMedID], nsv)
				writeToFile(pubMedID, result, out, paperID_h)


def main():  # many inputs! 
	parser = argparse.ArgumentParser(description="Find closest papers")
	parser.add_argument('--category', type=str, default="/projects/slin_prj/PubMed_Experiment/random_100_pubmed/data/random_PubMedIDs.txt",
		help="Path to the file with the list of randomly chosen PubMed IDs")
	parser.add_argument('--meta', type=str, default="/projects/slin_prj/PubMed_Experiment/random_100_pubmed/data/abstracts.txt", 
		help="Path to the file with paper metadata of all the papers in the matrix")
	parser.add_argument('--npaper', type=str, default="/projects/slin_prj/PubMed_Experiment/random_100_pubmed/data/getClosestAbstracts.log", 
		help="Log file for recording number of closest papers to find")
	parser.add_argument('--nsv', type=int, default=2000, help="Maximum number of singular values")
	parser.add_argument('--step', type=int, default=50, help="Size of the step of incrementation")
	parser.add_argument('--start', type=int, default=50, help="Minimum NSV")
	parser.add_argument('--nrow', type=int, default=12440, help="Number of rows in the matrix")
	
	parser.add_argument('--m', type=str, help="Path to the decomposed matrix")
	parser.add_argument('--s', type=str, help="Path to the singular values file")
	parser.add_argument('--out', type=str, help="Folder to write the file to")

	args = parser.parse_args()

	# Obtain a list and hashes to control our calculation 
	categories = getListOfTargets(args.category)  # a list of categories (PubMed IDs as strings)
	paperID_h = buildPaperHash(args.meta)	 	  # a hash of row number (integer) to PubMed ID (string)
	npapers_h = buildNumRetrivalsHash(args.npaper)# a hash of category (string) to number of papers to retrive (integer)

	# Make matrix and singular value array 
	matrix = readMatrix(args.m, args.nrow, args.nsv, args.out)
	svals = getSVals(args.s, args.nsv)
	matrix = scaleMatrix(matrix, svals)
	outputFile = args.out + '/{0}_{1}.neighbors'

	# try each different nsv, differ by args.step in each step 
	for nsv in range(args.step, args.nsv+1, args.step): 

		t = timeit.default_timer()
		outfile = outputFile.format('cosine', str(nsv))
		newM = normalizeMatrix(matrix, nsv)
		writeCosineResults(newM, outfile, categories, paperID_h, npapers_h, nsv)
		print "Time took to use cosine on " + str(nsv) + ": " + str(timeit.default_timer() - t)


		


if __name__ == '__main__':
	main()