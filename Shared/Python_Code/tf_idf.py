# convert term frequency file, generated by countFreq.py, to tf-idf
import argparse
import timeit 
import math


def tf_idf(termID, freq, nDocs, termDocFreqHash):
	# tf = math.log(1+freq, 10) # tfidf_logfreq
	# tf = freq # tfidf_raw
	# tf = 1  # binary 
	tf = 1 + math.log(freq, 10) # log of term frequency, add 1 smoothing to account for log(1) = 0
	idf = nDocs/float(termDocFreqHash[termID]) # inverse doc frequency
	idf = math.log(idf, 10) # log of idf 
	return round(tf*idf, 4) # arbitrarily round to 4 numbers after decimal place  


def freq_to_tfidf(termFreqFile, termDocFreqHash, nDocs, tfidf_out):
	with open(termFreqFile) as f, open(tfidf_out, 'w') as out:
		for line in f:
			if line != "\n": # paper has abstract with terms 
				pairs = line.strip().split('\t')
				line = ""
				for pair in pairs:
					[termId, freq] = pair.split(' ')
					score = tf_idf(int(termId), int(freq), nDocs, termDocFreqHash)
					line += ' '.join([termId, str(score)]) + '\t' 
			line = line.strip() # strip out the last tab 
			out.write(line+'\n') 	

def getTotalLines(fileName):
	lineNumber = 0
	with open(fileName) as f:
		for lineNum, line in enumerate(f):
			lineNumber = lineNum

	return lineNumber + 1 # Because lineNum is zerobase 


def buildTermDocFreqHash(filename):
	h = {}
	with open(filename, 'rb') as f:
		content = f.readlines()
		for line in content: 
			for pair in line.split('\t'):
				p = pair.split(' ')
				if len(p) == 2:
					h[int(p[0])] = h.get(int(p[0]), 0) + 1 # increment # docs by 1 
	return h


def main():

	parser = argparse.ArgumentParser(description='Convert matrix to a tf-idf Graphlab matrix')
	parser.add_argument('--t', type=str, help='Term-freq file')
	parser.add_argument('--tfidf', type=str, help="TF-IDF file")
	args = parser.parse_args()

	t = timeit.default_timer()
	termDocFreqHash = buildTermDocFreqHash(args.t)  # Build hash (termID: document frequency)
	print "\n Time took to build term freq hash: ", timeit.default_timer() - t

	nDocs = getTotalLines(args.t) # Get the total number of documents by counting # lines 
	 
	freq_to_tfidf(args.t, termDocFreqHash, nDocs, args.tfidf) # create tf-idf outdoc 
	

if __name__ == '__main__':
	main()