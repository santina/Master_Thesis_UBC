import sys
from os import listdir
from os.path import isfile, isdir, join
import re
import timeit
import argparse
from collections import defaultdict

"""
    This script summarize the information on multiple matrices given a range of singular values. Output file format header:
    matrix_name<num_{tf/tfidf}_rate_repetitionNum> \t forbenius \t maxAcceptableNSV \t variance \t nsv
    where maxAcceptableNSV is the maximum number of acceptable singular values judged by having low errors
"""

def main():
    # Parse and sanity check the inputs
    args = parse_args()

    # Create hashes for storing computed values
    forbeniusNorms = {} # matrix file name to forbenius norm.
    variances = defaultdict(list) # matrix file name to a list of (nsv, variances) tuples
    errorIndices = {} # matrix file to lowest error index

    # Calculate forbenius norm and errors for each matrix
    makeForbeniusHash(args.matrixFolder, forbeniusNorms)

    # Calculate the variance in each matrix and the maximum acceptable nsv.
    calculateVariances(args.svdFolder, args.min, args.max, args.step, variances, errorIndices)

    # Record the results
    writeResults(args.out, forbeniusNorms, errorIndices, variances)

def parse_args():
    """ Parsing input arguments """
    parser = argparse.ArgumentParser(description="Calculate forbenius norms on a folder of Graphlab result folders")
	parser.add_argument('--matrixFolder', type=str, help="folder with the matrices")
    parser.add_argument('--svdFolder', type=str, help="folder with the SVD result folders")
    parser.add_argument('--out', type=str, help="Out file to write the results to")
    parser.add_argument('--max', type=int, help="The maximum number of singular values")
    parser.add_argument('--min', type=int, help="The minimum number of singular values")
    parser.add_argument('--step', type=int, help="Step size of the number of singular values")
	args = parser.parse_args()

    if args.max <= args.min:
        print("Input error: max should be greater than min")
        sys.exit()

    return args

def makeForbeniusHash(folder, forbeniusNorms):
    """ Calculat forbenius norm for all matrix files inside `folder` """

    for matrixFile in [f for f in listdir(folder) if isfile(join(folder, f))]:
        filePath = join(folder, matrixFile)
        matrixName = matrixFile.replace(".matrix", "").replace(".sampled.", "_")
        forbeniusNorms[matrixName] = forbenius(filePath)

def frobenius(matrixfile):
    """ Given the same matrix file to GraphLab, return the forbenius norm.
    """
	frobenius = 0
	with open(matrixfile) as f:
		for _, line in enumerate(f): # 0 base for lineNum
			_, _, val = line.strip().split('\t')
			frobenius += float(val)**2
	return frobenius

def calculateVariances(folder, min_nsv, max_nsv, step_nsv, variances, errorIndices):
    """ Calculate the variances at various different singular values """

    # To into each svd folder
    for svdFolder in [f for f in listdir(folder) if isDir(join(folder, f))]:
        currFolder = join(folder, svdFolder)
        logfile = ""
        matrixName = svdFolder
        matrixName = matrixName.replace(".matrix.svd", "").replace(".sampled.", "_")

        # Obtain the log file for that folder of SVD outputs
        for f in [f for f in listdir(currFolder) if isFile(join(currFolder, f))]:
            if ".log" in f:
                logfile = join(currFolder, f)

        # Get the list of singular values and errors
        singularVals, errors = getSingularValues(logfile, 1000)  # TODO: make 1000 an input

        # Find the maximum acceptable nsv
        errorIndices[matrixName] = findIndexWLowerError(errors)

        # Calculate the variances for each nsv
        for nsv in range(min_nsv, max_nsv+1, step_nsv):
            variance = getSingularVariance(singularVals, nsv)
            variances[matrixName].append( (nsv, variance) )

def getSingularVariance(s, nranks=None):
    """ Get variance of the first 'nranks' of the singular value array """
	variance = 0

	if not nranks:
		nranks = len(s)
	for i in range(0, nranks):
		variance += s[i]**2

	return variance

def getSingularValues(logfile_path, nvalues):
    """ Read in the log file to get an array singluar value and an array of errors
    """
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

def findIndexWLowerError(array, start=0):
	for i in range(start, len(array)):
		if 'e' not in str(array[i]):
			return i

def writeResults(outfile, forbeniusNorms, errorIndices, variance):

    out = open(outfile, "w")

    # loop through each matrix
    for matrixName in forbeniusNorms.keys():
        forbenius = forbeniusNorms[matrixName]
        maxNSV = errorIndices[matrixName]
        for pair in variances[matrixName]:
            nsv, variance = pair[0], pair[1]
            result = '\t'.join([matrixName, forbenius, maxNSV, variance, nsv])
            out.write(result + '\n')

    out.close()

if __name__ == '__main__':
    main()
