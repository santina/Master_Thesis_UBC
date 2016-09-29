# Checking the differences between two termID-frequency files
from itertools import izip
import argparse

def main():
    parser = argparse.ArgumentParser(description='As manual inspection can be difficult \
    given that termID-frequency pairs are not always in ordered, this script is used to \
    check the difference between two termID-frequency files.')
    parser.add_argument('--f1', type=str, help='First termID-frequency file')
    parser.add_argument('--f2', type=str, help='Another termID-frequency file to check against f1.')
    parser.add_argument('--out', type=str, help='Output file summarizing the result')
    args = parser.parse_args()

    out = open(args.out, 'w')
    checkDifference(args.f1, args.f2, out)


def createDefaultDict(line):
    """ Turn a line in the termID-frequency file into a termID-frequency dictionary """
    d = {}
    if line == "\n":
        return d
    line = line.strip().split('\t')
    for pair in line:
         key, val = pair.split()
         d[key] = val
    return d


def findXOR(d1, d2):
    """ Find the key-value pairs in d1 but not in d2, or with different value in d2.
    return the differences recorded as a dictionary
    """
    diff = {}
    for key in d1.keys():
        if d2.has_key(key):
            if d2[key] == d1[key]:
                continue
        diff[key] = d1[key]
    return diff


def hashAsString(dictionary):
	""" Convert a dictionary to a string
	@input:
		a dicitonary of termID : frequencies
	@output:
		a string representing the dictionary, each key-value pair is separated
		by a tab deliminator, and key and value
		themselves are separated by a space
	"""
	string = ""

	for key, val in dictionary.iteritems():
		string += ' '.join([str(key), str(val)]) + "\t"

	return string.strip() # strip out the last tab


def findDifference(d1, d2):
    # Find the key-value pairs in d1 but not in d2
    diff_d1_d2 = hashAsString( findXOR(d1, d2) )
    # Find the key value pairs in d2 but not in d1
    diff_d2_d1 = hashAsString( findXOR(d2, d1) )

    if diff_d1_d2 == "" and diff_d2_d1 == "":
        return ""
    else:
        return 'File 1 - ' + diff_d1_d2 + " File 2 - " + diff_d2_d1


def writeInfo(file1, file2, out):
    info = ""
    info += "File 1 : " + file1 + '\n'
    info += "File 2 : " + file2 + '\n'
    info += "Differeces are noted by line number, followed by the differences. \n"
    info += "Annotations: * means f1 has more key-value pair, ~ means f2 has more. \n"
    info += "==================================================================\n"

    out.write(info)

def determineSymbol(d1, d2):
    symbol = ""
    if len(d1) > len(d2):
        symbol = '*'
    elif len(d2) > len(d1):
        symbol = '~'
    return symbol

def checkDifference(file1, file2, out):
    writeInfo(file1, file2, out)

    lineNum = 1
    numDifferences = 0
    with open(file1) as f1, open(file2) as f2:
        for l1, l2 in izip(f1, f2):
            d1 = createDefaultDict(l1)
            d2 = createDefaultDict(l2)
            difference = findDifference(d1, d2)
            if difference != "":
                symbol = determineSymbol(d1, d2)
                out.write(symbol + str(lineNum) + ': ' + difference + '\n')
                numDifferences += 1
            # Clean up
            del d1
            del d2

            lineNum += 1

    out.write("==================================================================\n")
    out.write("Total number of differences : " + str(numDifferences) + '\n')

if __name__ == '__main__':
	main()
