
import os, os.path # accessing files and folders 
import argparse    # parsing command line args 


def getIDs(abstractFile):
	ids = []
	with open(abstractFile) as f:
		for line in f:
			line = line.split('\t')
			ids.append(line[0])
	return ids 

def getAllIDs(folder, outfile): 
	out = open(outfile, "w")
	files = [f for f in os.listdir(folder) if os.path.isfile(os.path.join(folder, f))]
	
	for f in files:
		f = os.path.join(folder, f)
		ids = getIDs(f)
		out.write(' '.join(ids) + '\n')

def main():
	parser = argparse.ArgumentParser(description='Make a file with all the pmids')
	parser.add_argument('--f', type=str, help='file that has all the medline abstract files')
	parser.add_argument('--out', type=str, help='file to write all the pmids to')
	args = parser.parse_args()

	getAllIDs(args.f, args.out)


if __name__ == '__main__':
	main()