# Evaluate number of singular values to keep
# input file is the log file from GraphLab, we want to see the variance coverage on the choice of nsv

import numpy as np
import random
import argparse

def main():
	args = parse_arguments()
	frob = frobenius(args.m)
	sv = get_singular_values(args.s, args.n)
	print "Forbenius: " + str(frob)
	variance = getSingularVariance(sv)
	print "Variance: " + str(variance)
	print "Coverage: " + str(variance/frob)

def parse_arguments():
	parser = argparse.ArgumentParser(description='')
	parser.add_argument('--log', type=str, help='Log file from running GraphLab. It contains singular values and their errors.')
	parser.add_argument('--s', type=str, help="singular value file")
	parser.add_argument('--m', type=str, help='Matrix file')
	parser.add_argument('--n', type=int, help='Number of singular values')

	return parser.parse_args()

# Get variance of the input matrix
def getMatrixVariance(matrix):
	variance = 0
	for r in range(0, matrix.shape[0]):
		for c in range(0, matrix.shape[1]):
			variance += matrix[r][c]**2
	return variance

# Get variance of the first 'nranks' of the singular value array
def getSingularVariance(s, nranks=None):
	variance = 0

	if not nranks:
		nranks = len(s)

	for i in range(0, nranks):
		variance += s[i]**2

	return variance

# Input : same matrix file to GraphLab
def frobenius(matrixfile):
	frobenius = 0

	with open(matrixfile) as f:
		for _, line in enumerate(f): # 0 base for lineNum
			_, _, val = line.strip().split('\t')
			frobenius += float(val)**2
	return frobenius


# Read in the log file to get an array singluar value and an array of errors
def get_singular_values_from_log(logfile_path, nvalues):
	singularVals = []
	errors = []
	count = 0

	with open(logfile_path) as f:
		for _, line in enumerate(f): # 0 base for lineNum
			if "Singular value" in line:
				content = line.split()
				singularVals.append(float(content[3]))
				errors.append(float(content[6]))
				count += 1
				if count == nvalues:
					break


	assert len(errors) == len(singularVals)
	return singularVals, errors

def get_singular_values(singular_val_file, nvalues):
	singularVals = []
	nsv = 0
	with open(singular_val_file) as f:
		for line in f:
			if nsv >= nvalues:
				break
			try:
				singularVals.append(float(line))
				nsv += 1
			except:
				pass # omid the first line of the file, descriptor of the file

	return singularVals


def findIndexWLowerError(array, start=0):
	for i in range(start, len(array)):
		if 'e' not in str(array[i]):
			return i


if __name__ == '__main__':
	main()
