# Find the target pmids for the second level pmids. This is likely to be a one-time use script 
import argparse 
import timeit

def makeTargetHash(answerFile, idFile):
	
	ids_targets_hash = {} 

	targets = []
	with open(answerFile) as f:
		for row in f:
			targets.append(row.split()[0])

	with open(idFile) as f:
		for index, row in enumerate(f):
			second_level_IDs = row.strip().split()
			ids_targets_hash[targets[index]] = second_level_IDs

	return ids_targets_hash

def findTarget(targetHash, second_level_id):
	for key in targetHash.keys():
		if second_level_id in targetHash[key]:
			return key 


def write_w_target(targetHash, outfile, abstractFile):
	out = open(outfile, 'w')
	with open(abstractFile) as f:  
		for line in f:
			second_level_id = line.split()[0]
			targetID = findTarget(targetHash, second_level_id)
			
			info = '\t'.join([targetID, line])
			out.write(info)
	out.close()



def main():
	parser = argparse.ArgumentParser(description="Find the target pmid for each second level closest abstracts")
	parser.add_argument('--f', type=str, help='abstract file without the target pmids', 
		default="/projects/slin_prj/PubMed_Experiment/shallow_vs_deep/data_closest_papers/abstracts/secondLevel.abstracts")
	
	parser.add_argument('--a', type=str, help='Answer key', 
		default="/projects/slin_prj/PubMed_Experiment/shallow_vs_deep/data_closest_papers/pmids/closestPaperIDs.txt")

	parser.add_argument('--ids', type=str, help='Answer key', 
		default="/projects/slin_prj/PubMed_Experiment/shallow_vs_deep/data_closest_papers/pmids/closestPaperIDs_second_noFirstLevel.txt")
	
	parser.add_argument('--o', type=str, help='New file with the target pmids', 
		default="/projects/slin_prj/PubMed_Experiment/shallow_vs_deep/data_closest_papers/abstracts/secondLevel.abstracts.wtarget")
	
	args = parser.parse_args()

	t = timeit.default_timer()
	targetHash = makeTargetHash(args.a, args.ids)
	print "Took ", timeit.default_timer() - t, "seconds to make the hash."

	t = timeit.default_timer()
	write_w_target(targetHash, args.o, args.f )
	print "Took ", timeit.default_timer() - t, "seconds to find all the targets."

if __name__ == '__main__':
	main()