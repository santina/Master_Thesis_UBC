# Combine the files in /projects/slin_prj/PubMed_Experiment/categories 
# each file:  PMID Title AbstractText 
# Written in Python 3 

import argparse 
from os import listdir
from os.path import isfile, isdir, join
from sets import Set

def concate(abstractFolder, outFileObject):
	''' Combine files content by copying the content in `abstractFolder` to `outFileObject
	'''

	idHash = Set([])
	for abstractfile in [f for f in listdir(abstractFolder) if isfile(join(abstractFolder, f))]:
		curFile = join(abstractFolder, abstractfile)
		

		# Open the file and write the needed content to the outfile object 
		with open(curFile) as f:
			for lineNum, line in enumerate(f):
				line = line.strip().split('\t')
				try:
					pubmedID, title, abstract = line[0], line[1], line[2]
				except IndexError:
					print curFile
					break # Go to the next file 
				if int(pubmedID) not in idHash: 
					idHash.add(int(pubmedID))
					outString = '\t'.join([abstractfile, pubmedID, title, abstract])  # filename, pubmedID, title, abstract 
					outFileObject.write(outString + '\n')


def main():
	parser = argparse.ArgumentParser(description='')
	parser.add_argument('--f', type=str, help='Folder with all the files')
	parser.add_argument('--out', type=str, help='File to write the result to')



	args = parser.parse_args()
	out = open(args.out, 'w')
	concate(args.f, out)
	out.close()


if __name__ == '__main__':
	main()