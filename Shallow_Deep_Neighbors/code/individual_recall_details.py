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

def getRecall(relatedIDs, correct_papers, other_predictions, missed_predictions, correct_predictions):
	''' Calculate how many related paper IDs calculated by SVD are in the answer key
	and return the value divided by total number of retrived IDs 
	'''
	recalls = 0
	numPapers = len(relatedIDs)

	for i in relatedIDs:
		if i in correct_papers:
			correct_predictions.append(i)
			recalls += 1
		else: 
			other_predictions.append(i)

	for i in correct_papers:
		if i not in relatedIDs:
			missed_predictions.append(i)

	return float(recalls)/numPapers


def record(answer_keys, result_file, out_file, out_file2, correct_file):
	''' Record the precision for each paper
	'''

	out_new = open(out_file, 'w')
	out_missed = open(out_file2, 'w')
	out_correct = open(correct_file, 'w')
	with open(result_file) as f:

		for line in f:

			other_predictions = []  # Record papers IDs that are not in the answer key
			missed_predictions = [] # Record papers IDs that are in the answer key but not in the predictions
			correct_predictions = []

			line = line.strip().split("\t")   # targetID  \t  (related target paper IDs)
			
			targetID = line[0]
			relatedIDs = line[1].split() # include the target ID
			
			score = getRecall(relatedIDs, answer_keys[targetID], other_predictions, missed_predictions, correct_predictions)
			total = len(relatedIDs)

			n_predictions = len(other_predictions)
			other_predictions = ' '.join(other_predictions)

			n_missed = len(missed_predictions)
			missed_predictions = ' '.join(missed_predictions)

			n_correct = len(correct_predictions)
			correct_predictions = ' '.join(correct_predictions)


			out_new.write('\t'.join([targetID, str(score), str(total), str(n_predictions), other_predictions]) + '\n')
			out_missed.write('\t'.join([targetID, str(score), str(total), str(n_missed), missed_predictions]) + '\n')
			out_correct.write('\t'.join([targetID, str(score), str(total), str(n_correct), correct_predictions]) + '\n')

def main():
	parser = argparse.ArgumentParser(description="Evaluating Pubmed results in more details")
	parser.add_argument('--a', type=str, help='file with the correct answers')
	parser.add_argument('--f', type=str, help='The result file')
	parser.add_argument('--out', type=str, help='Out file to write the results to for new predictions')
	parser.add_argument('--out2', type=str, help='Out file to write the results to for missed predictions')
	parser.add_argument('--out3', type=str, help='Outfile to write the correct predictions')
	args = parser.parse_args()

	answer_keys = buildClosestPapersHash(args.a)
	record(answer_keys, args.f, args.out, args.out2, args.out3)

if __name__ == '__main__':
	t = timeit.default_timer()
	main()
	print "Evaluation took ", str(timeit.default_timer() - t), " seconds"
