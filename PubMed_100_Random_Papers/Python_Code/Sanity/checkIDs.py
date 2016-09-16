
import argparse
from os import listdir
from os.path import isfile, isdir, join

def matchID(folder, papersIDfile):
 	''' Check if the IDs match to make sure that in `papersIDfile`, which records
 	the closest papers' IDs to each ID  
 	the first ID is the category ID (target paper), where category IDs are the file
 	name in `folder` 
 	'''

	filenames = []
	categoriesID = []
	for filename in [f for f in listdir(folder) if isfile(join(folder, f))]:
		filenames.append(filename)
	with open(papersIDfile) as f:
		for line in f:
			line = line.split()
			categoriesID.append(line[0])  # The first one is the target 

	print len(filenames)
	print len(categoriesID)

	for i in filenames:
		if i not in categoriesID:
			print "Fail"

def main():

	parser = argparse.ArgumentParser(description='')
	parser.add_argument('--f', type=str, help='folder with the files')
	parser.add_argument('--a', type=str, help='closest Paper ID files')
	args = parser.parse_args()	

	matchID(args.f, args.a)

if __name__ == '__main__':
	main()