# Remove duplicated IDs between 1st and 2nd level of IDs of each targetID 
# each file:  PMID Title AbstractText 

import argparse 
from sets import Set


def createListofSets(firstLevelIDsFile):
	listOfSets = []

	with open(firstLevelIDsFile) as f:
		for line in f:
			idHash = Set([])
			line = line.strip().split()
			IDs = [int(ID) for ID in line]
			for ID in IDs:
				idHash.add(ID)
			listOfSets.append(idHash)
	return listOfSets


def check(listOfSets, ID):
	for h in listOfSets:
		if ID in h:
			return 0
	return 1


def writeToFile(outFileObject, IDs):
	outFileObject.write(' '.join([str(i) for i in IDs]) + '\n')


def removeDuplicates(firstLevelIDsFile, secondLevelIDsFile, outfile):
	''' Combine files content by copying the content in `abstractFolder` to `outFileObject
	'''
	hs = createListofSets(firstLevelIDsFile) # a list of sets of IDs

	repeats = [] #for debugging 

	# Open the file and write the needed content to the outfile object 
	with open(secondLevelIDsFile) as f, open(outfile, 'w') as out:
		for line in f:

			line = line.strip().split() # Each ID in each line is separated by a space 
			IDs = [int(ID) for ID in line]
			keptIDs = []
			
			for ID in IDs: # Skip the first ID
				if check(hs, ID):
					keptIDs.append(ID)
				else: 
					repeats.append(ID)

			writeToFile(out, keptIDs)

	print "there are this many repeats", len(repeats)


def main():
	parser = argparse.ArgumentParser(description='')
	parser.add_argument('--f1', type=str, help='first level ID file')
	parser.add_argument('--f2', type=str, help="second level ID file")
	parser.add_argument('--out', type=str, help='second level ID file with no IDs occur in the first level ID file')

	args = parser.parse_args()

	removeDuplicates(args.f1, args.f2, args.out)
	


if __name__ == '__main__':
	main()