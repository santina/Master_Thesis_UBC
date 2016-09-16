# Remove duplicated IDs in the 1st of closest neighbors of the randomly selected target IDs 
# each file:  PMID Title AbstractText 

import argparse 
from sets import Set

def writeToFile(outFileObject, IDs):
	outFileObject.write(' '.join([str(i) for i in IDs]) + '\n')


def removeDuplicates(IDfile, outfile):
	''' Combine files content by copying the content in `abstractFolder` to `outFileObject
	'''

	idHash = Set([])
	repeated = [] # for debugging 
	
	# Open the file and write the needed content to the outfile object 
	with open(IDfile) as f, open(outfile, 'w') as out:
		for line in f:
			line = line.strip().split() # Each ID in each line is separated by a space 
			keptIDs = [int(line[0])] # the IDs that will be written to the new file, keep the first ID, which is the target for all other IDs  
			
			for ID in line[1:]: # Skip the first ID
				pmid = int(ID) # cast it to int to reduce memory need 
				
				if pmid not in idHash:
					idHash.add(pmid)
					keptIDs.append(pmid)
				else:
					repeated.append(pmid) 

			writeToFile(out, keptIDs)

	# For debugging 
	print "these are the repeated IDs"
	print repeated 
	print len(repeated)


def main():
	parser = argparse.ArgumentParser(description='')
	parser.add_argument('--f', type=str, help='ID file')
	parser.add_argument('--out', type=str, help='ID file with no repeated IDs')

	args = parser.parse_args()
	
	removeDuplicates(args.f, args.out)
	


if __name__ == '__main__':
	main()