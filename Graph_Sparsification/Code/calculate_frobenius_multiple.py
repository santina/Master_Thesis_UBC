import sys
from os import listdir
from os.path import isfile, isdir, join
import re
import timeit
import argparse
from collections import defaultdict
import math

"""
    This script summarize the information on multiple matrices given a range of singular values. Output file format header:
    matrix_name<num_{tf/tfidf}_rate_repetitionNum> \t frobenius \t maxAcceptableNSV \t variance \t nsv
    where maxAcceptableNSV is the maximum number of acceptable singular values judged by having low errors
"""

def main():
    # Parse and sanity check the inputs
    args = parse_args()

    # Create hashes for storing computed values
    frobeniusNorms = {} # matrix file name to frobenius norm.
    frobenius_norms = defaultdict(list) # matrix file name to a list of (nsv, frobenius_norm) tuples
    errorIndices = {} # matrix file to lowest error index

    # Calculate frobenius norm and errors for each matrix
    print("Calculating frobenius norms for all the matrices.")
    makefrobeniusHash(args.matrixFolder, frobeniusNorms)

    # Calculate the variance in each matrix and the maximum acceptable nsv.
    print("Calculating frobenius norms in the SVD results.")
    calculateSingularFrobenius(args.svdFolder, args.min, args.max, args.step, frobenius_norms, errorIndices)

    # Record the results
    print("Writing results to the out file.")
    writeResults(args.out, frobeniusNorms, errorIndices, frobenius_norms)

def parse_args():
    """ Parsing input arguments """
    parser = argparse.ArgumentParser(description="Calculate frobenius norms on a folder of Graphlab result folders")
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

def makefrobeniusHash(folder, frobeniusNorms):
    """ Calculate frobenius norm for all matrix files inside `folder` """

    for matrixFile in [f for f in listdir(folder) if isfile(join(folder, f))]:
        filePath = join(folder, matrixFile)

        matrixFile = matrixFile.replace(".matrix", "")

        frobeniusNorms[matrixFile] = frobenius(filePath)

def frobenius(matrixfile):
    """ Given the same matrix file to GraphLab, return the frobenius norm.
    """
    frobenius = 0
    with open(matrixfile) as f:
    	for _, line in enumerate(f): # 0 base for lineNum
    		_, _, val = line.strip().split('\t')
    		frobenius += float(val)**2
    frobenius = math.sqrt(frobenius)
    return frobenius

def calculateSingularFrobenius(folder, min_nsv, max_nsv, step_nsv, frobenius_norms, errorIndices):
    """ Calculate the frobenius norms at various different singular values """

    # To into each svd folder
    for svdFolder in [f for f in listdir(folder) if isdir(join(folder, f))]:
        currFolder = join(folder, svdFolder)
        logfile = ""
        matrixName = svdFolder.replace(".matrix.svd", "")
        # Obtain the log file for that folder of SVD outputs
        for f in [f for f in listdir(currFolder) if isfile(join(currFolder, f))]:
            if ".log" in f:
                logfile = join(currFolder, f)

        # Get the list of singular values and errors
        singularVals, errors = getSingularValues(logfile, 1500)  # TODO: make NSV an input

        # Find the maximum acceptable nsv, skipping the first because the first singular
        # have higher error rate.
        errorIndices[matrixName] = findIndexWLowerError(errors, 1)

        print matrixName
        # Calculate the frobenius norms for each nsv

        for nsv in range(min_nsv, max_nsv+1, step_nsv):
            print nsv
            actual_nsv, variance = getSingularFrobenius(singularVals, nsv)
            if nsv > len(singularVals):
                frobenius_norms[matrixName].append( (len(singularVals), variance) )
                break
            frobenius_norms[matrixName].append( (nsv, variance) )

def getSingularFrobenius(s, nranks=None):
    """ Get variance of the first 'nranks' of the singular value array """
    frobenius = 0
    actual_nsv = 0

    if not nranks:
    	nranks = len(s)
    for i in range(0, nranks):
        try:
            frobenius += s[i]**2
            actual_nsv += 1
        except IndexError:
            break

    frobenius = math.sqrt(frobenius)
    return actual_nsv, frobenius

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

def writeResults(outfile, frobeniusNorms, errorIndices, frobenius_norms):

    out = open(outfile, "w")

    # Write header
    header = "\t".join(["matrix_name", "matrix_norm", "maxAcceptableNSV", "frobenius", "nsv"])
    out.write(header + '\n')

    # loop through each matrix
    for matrixName in frobeniusNorms.keys():
        matrix_norm = frobeniusNorms[matrixName]
        maxNSV = errorIndices[matrixName]
        for pair in frobenius_norms[matrixName]:
            nsv, forbenius_norm = pair[0], pair[1]
            result = '\t'.join([matrixName, str(matrix_norm), str(maxNSV), str(forbenius_norm), str(nsv)])
            out.write(result + '\n')

    out.close()

if __name__ == '__main__':
    main()
