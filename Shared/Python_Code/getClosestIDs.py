# Get closest paper IDs 
import argparse 
import time
from Bio import Entrez


def writeClosestIDs(IDFile, outfile):
	''' Read each line, which is a ID, and obtain the IDs of its related papers
	'''
	with open(IDFile) as f, open(outfile, 'w') as out:
		for line in f:
			info = ""
			related_info = Entrez.read(Entrez.elink(dbfrom='pubmed', db='pubmed', id=line.strip()))
			related_papers = related_info[0]['LinkSetDb'][0]['Link']
			for ID in related_papers:
				info += ID["Id"] + ' '
			out.write(info.strip() + '\n')
			time.sleep(0.5)  # to ensure we don't overload it 

def main():

	parser = argparse.ArgumentParser(description='Get a number of random pubmed IDs and save that to a file')
	parser.add_argument('--f', type=str, help='file that has all the IDs')
	parser.add_argument('--out', type=str, help='File to write the result to')
	parser.add_argument('--email', type=str, help="Email for using Entrez.Bio")
	args = parser.parse_args()

	# Set my email 
	Entrez.email = args.email

	# Find closest paper IDs for each paper (ID)
	writeClosestIDs(args.f, args.out)


if __name__ == '__main__':
	main()
