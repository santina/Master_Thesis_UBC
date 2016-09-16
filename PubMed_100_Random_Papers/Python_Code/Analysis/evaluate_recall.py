# Evaluate the recall/precision given a result folder 

from os import listdir
from os.path import isfile, isdir, join
import re 
import timeit
import argparse 

def buildClosestPapersHash(answer_file):
	''' Build and return a dictionary that maps target paper ID (key, as a string) to 
	a list of closest papers IDs (strings)
	'''
	h = {}
	with open(answer_file) as f:
		for line in f:
			line = line.strip().split()
			h[line[0]] = line 

	return h

def getRecall(relatedIDs, correct_papers):
	''' Calculate how many related paper IDs calculated by SVD are in the answer key
	and return the value divided by total number of retrived IDs 
	'''
	recalls = 0
	numPapers = len(relatedIDs)

	for i in relatedIDs:
		if i in correct_papers:
			recalls += 1

	return float(recalls)/numPapers


def getScore(current_file, answer_keys):
	''' Get the average precision of the predictions by checking whether 
	the papers in the prediction are of the same as PubMed 
	'''
	with open(current_file) as f:
		totalScore = 0
		totalPapers = 0
		for line in f:
			line = line.strip().split("\t")   # targetID  \t  (related target paper IDs)
			
			targetID = line[0]
			relatedIDs = line[1].split() # include the target ID
			
			score = getRecall(relatedIDs, answer_keys[targetID])
			
			totalScore += score 
			totalPapers += 1
			
			
	return float(totalScore)/totalPapers


def recordScore(out, score, matrixFolder, distanceFolder, closestPapersFile):
	''' Write the average score for a particular combination of a type matrix, a distance function, 
	and number of singular values used to an outfile file `out` 
	'''
	
	nsv = re.findall(r'\d+', closestPapersFile)[0]
	out.write('\t'.join([matrixFolder, distanceFolder, nsv, str(score)]) + '\n')


def traverseFile(resultFolder, answer_keys, evalResultOutFile):
	''' Go through all the folders in the `resultFolder`, extract the name as the type of 
	matrix or similarity measurement, and calculate precision for each file write 
	to `evalResultOutFile` 
	'''
	# file organization: 
	# resultFolder 
	#	> (type of matrix) {term_freq, term_freq_binary, tf_idf} 
	#		> (type of distance measurement) {euclidean, cosine}
	out = open(evalResultOutFile, 'w')
	
	for matrixFolder in [f for f in listdir(resultFolder) if isdir(join(resultFolder, f))]:
		curDir = join(resultFolder, matrixFolder)
		
		for distanceFolder in [f for f in listdir(curDir) if isdir(join(curDir, f))]:
			curFolder = join(curDir, distanceFolder)

			for closestPapersFile in [f for f in listdir(curFolder) if isfile(join(curFolder, f))]:
				currentFile = join(curFolder, closestPapersFile)
				
				score = getScore(currentFile, answer_keys)  # Get recall or precision 
				recordScore(out, score, matrixFolder, distanceFolder, closestPapersFile)


def main():
	parser = argparse.ArgumentParser(description="Evaluating Pubmed results")
	parser.add_argument('--a', type=str, help='file with the correct answers')
	parser.add_argument('--f', type=str, help='The result folder')
	parser.add_argument('--out', type=str, help='Out file to write the results to')
	args = parser.parse_args()

	answer_keys = buildClosestPapersHash(args.a)

	traverseFile(args.f, answer_keys, args.out)

if __name__ == '__main__':
	t = timeit.default_timer()
	main()
	print "Evaluation took ", str(timeit.default_timer() - t), " seconds"
