import sys
import re
import timeit
import argparse
from collections import defaultdict

"""
    Generate a R data.frame friendly text file with two columns : nsv and coverage
"""

def main():
    # Parse and sanity check the inputs
    args = parse_args()

    record_coverage(args.m, args.s, args.min, args.max, args.step, args.out)

def parse_args():
    """ Parsing input arguments """
    parser = argparse.ArgumentParser(description="Calculate forbenius norms on a folder of Graphlab result folders")
    parser.add_argument('--m', type=str, help="folder with the matrices")
    parser.add_argument('--s', type=str, help="folder with the SVD result folders")
    parser.add_argument('--out', type=str, help="Out file to write the results to")
    parser.add_argument('--max', type=int, help="The maximum number of singular values")
    parser.add_argument('--min', type=int, help="The minimum number of singular values")
    parser.add_argument('--step', type=int, help="Step size of the number of singular values")
    args = parser.parse_args()

    if args.max <= args.min:
        print("Input error: max should be greater than min")
        sys.exit()

    return args

def record_coverage(matrix, svals, min_nsv, max_nsv, step, out):
    print(str(min_nsv) + " " + str(max_nsv) + " " + str(step))
    frobenius_norm = frobenius(matrix)
    print("Done with the big matrix")
    print(str(frobenius_norm))

    singular_values = getSingularValues(svals, max_nsv)
    print(len(singular_values))
    variance = 0
    start_index = 0
    with open(out, "w") as outfile:
        outfile.write("nsv \t coverage \t variance" + "\n")
        for i in range(min_nsv, max_nsv+1, step):
            print(i)
            variance = sum([s**2 for s in singular_values[0:i+1]])
            coverage = float(variance)/frobenius_norm
            outfile.write(str(i) + "\t" + str(coverage) + "\t" + str(variance) +  "\n")





def frobenius(matrixfile):
    """ Given the same matrix file to GraphLab, return the forbenius norm.
    """
    frobenius = 0
    with open(matrixfile) as f:
    	for _, line in enumerate(f): # 0 base for lineNum
    		_, _, val = line.strip().split('\t')
    		frobenius += float(val)**2
    return frobenius

def calculateVariances(svals, start_nsv, end_nsv):
    return sum([s**2 for s in svals[start_nsv:end_nsv+1]])


def getSingularValues(logfile_path, nvalues):
    """ Read in the log file to get an array singluar value and an array of errors
    """
    singularVals = []
    count = 0

    with open(logfile_path) as f:
    	for _, line in enumerate(f): # 0 base for lineNum
    		if "Singular value" in line:
    			content = line.split()
    			singularVals.append(float(content[3]))
    			count += 1
    			if count == nvalues:
    				break

	return singularVals



if __name__ == '__main__':
    main()