import re
from lingpipe import LingPipe
from geniatagger import GeniaTagger
import HTMLParser
import unicodedata
import xml.etree.ElementTree as etree
import os.path
import codecs
import pickle

# Wrappers for GeniaTagger and LingPipe scripts. Loaded with loadParsingTools()
tagger = None
lingpipe = None

# Instantiate the wrappers for various parse tools
def loadParsingTools():
	global tagger, lingpipe
	# Currently point to scripts. TODO: use $PATH instead to find them	
	tagger = GeniaTagger('/home/jlever/apps/geniatagger-3.0.1/geniatagger')
	lingpipe = LingPipe('/projects/jlever/megaTextProject/nounphrasePipeline/lingpipeSentenceSplitter/run.sh')

# Simple sentence splitter wrapper that calls Lingpipe
def sentenceSplit(text):
	return lingpipe.parse(text)

# Remove control characters from text and some other weird stuff
def handleEncoding(text):
	# Remove some "control-like" characters (left/right separator)
	text = text.replace(u'\u2028',' ').replace(u'\u2029',' ')
	text = "".join(ch for ch in text if unicodedata.category(ch)[0]!="C")
	text = text.encode('utf8')
	return text.strip()
	
# Unescape HTML special characters e.g. &gt; is changed to >
htmlParser = HTMLParser.HTMLParser()
def htmlUnescape(text):
	return htmlParser.unescape(text)
	
# Remove empty brackets (that could happen if the contents have been removed already
# e.g. for citation ( [3] [4] ) -> ( ) -> nothing
def removeBracketsWithoutWords(text):
	fixed = re.sub(r'\([\W\s]*\)', ' ', text)
	fixed = re.sub(r'\[[\W\s]*\]', ' ', fixed)
	fixed = re.sub(r'\{[\W\s]*\}', ' ', fixed)
	return fixed
	
# Some older articles have titles like "[A study of ...]."
# This removes the brackets while retaining the full stop
def removeWeirdBracketsFromOldTitles(titleText):
	titleText = titleText.strip()
	if titleText[0] == '[' and titleText[-2:] == '].':
		titleText = titleText[1:-2] + '.'
	return titleText
	
def getMaxWordLength(text):
	words = text.split()
	wordLengths = [ len(w) for w in words ]
	return max(wordLengths)

# Tokenize text into a tuple of the word/tokens
def tokenize(text):
	if text == '':
		return tuple()
		
	# Do a basic test for crazy length words
	maxWordLength = getMaxWordLength(text)
	if maxWordLength >= 900:
		return tuple()

	try:
		parse = tagger.parse(text.strip())
	except IOError, e:
		# Reraise the IO error with more context
		raise IOError('Error passing information to GeniaTagger subprocess. Likely that GeniaTagger has crashed.')
	tokens = []
	for (w,_,_,iob,_) in parse:
		tokens.append(w)
	return tuple(tokens)
	
# Extract the noun-phrases from a sentence and return them
# as a list of lists of tokens
def extractNounphrasesFromSentence(sentence):
	parse = tagger.parse(sentence.strip())
	nounphrases = []
	current = []
	for (w,_,_,iob,_) in parse:
		if iob == 'B-NP' or iob == 'I-NP':
			current.append(w.lower())
		elif len(current) > 0:
			nounphrases.append(current)
			current = []
	if len(current) > 0:
		nounphrases.append(current)

	return nounphrases
	


def unicodeLower(str):
	return str.decode('utf8').lower().encode('utf8')
	
# Given a tokenized bit of text, find all the words that
# are in a lookup dictionary. Find longest terms first.
def getID_FromLongestTerm(np, lookupDict):
	terms = []
	# Lowercase all the tokens
	np = [ unicodeLower(w) for w in np ]
	
	# The length of each search string will decrease from the full length
	# of the text down to 1
	for l in reversed(range(1, len(np)+1)):
		# We move the search window through the text
		for i in range(len(np)-l+1):
			# Extract that window of text
			s = tuple(np[i:i+l])
			# Search for it in the dictionary
			if s in lookupDict:
				# If found, save the ID in the dictionary
				terms.append(lookupDict[s])
				# And blank it out
				np[i:i+l] = [ "" for _ in range(l) ]
				
	# Then return the found term IDs
	return terms
	
# Code for extracting text from Medline/PMC XML files

# XML elements to ignore the contents of
ignoreList = ['table', 'xref', 'disp-formula', 'inline-formula', 'ref-list']

# XML elements to separate text between
separationList = ['title', 'p', 'sec']
def extractTextFromElem(elem):
	textList = []
	
	# Extract any raw text directly in XML element or just after
	head = ""
	if elem.text:
		head = elem.text
	tail = ""
	if elem.tail:
		tail = elem.tail
	
	# Then get the text from all child XML nodes recursively
	childText = []
	for child in elem:
		childText = childText + extractTextFromElem(child)
		
	# Check if the tag should be ignore (so don't use main contents)
	if elem.tag in ignoreList:
		return [tail.strip()]
	# Add a zero delimiter if it should be separated
	elif elem.tag in separationList:
		return [0] + [head] + childText + [tail]
	# Or just use the whole text
	else:
		return [head] + childText + [tail]
	

# Merge a list of extracted text blocks and deal with the zero delimiter
def extractTextFromElemList_merge(list):
	textList = []
	current = ""
	# Basically merge a list of text, except separate into a new list
	# whenever a zero appears
	for t in list:
		if t == 0: # Zero delimiter so split
			if len(current) > 0:
				textList.append(current)
				current = ""
		else: # Just keep adding
			current = current + " " + t
			current = current.strip()
	if len(current) > 0:
		textList.append(current)
	return textList
	
# Main function that extracts text from XML element or list of XML elements
def extractTextFromElemList(elemList):
	textList = []
	# Extracts text and adds delimiters (so text is accidentally merged later)
	if isinstance(elemList, list):
		for e in elemList:
			textList = textList + extractTextFromElem(e) + [0]
	else:
		textList = extractTextFromElem(elemList) + [0]

	# Merge text blocks with awareness of zero delimiters
	mergedList = extractTextFromElemList_merge(textList)
	return mergedList
	
# Process a MEDLINE abstract file
# Pass in the file object, the mode to parse it with and whether to merge the output
def processAbstractFile(abstractFile, outFile, processFunction):
	count = 0
	
	# These XML files are huge, so skip through each MedlineCitation element using etree
	for event, elem in etree.iterparse(abstractFile, events=('start', 'end', 'start-ns', 'end-ns')):
		if (event=='end' and elem.tag=='MedlineCitation'):
			count = count + 1
			
			# Find the elements for the PubMed ID, and publication date information
			pmid = elem.findall('./PMID')
			yearFields = elem.findall('./Article/Journal/JournalIssue/PubDate/Year')
			medlineDateFields = elem.findall('./Article/Journal/JournalIssue/PubDate/MedlineDate')

			# Try to extract the pmidID
			pmidText = ''
			if len(pmid) > 0:
				pmidText = " ".join( [a.text.strip() for a in pmid if a.text ] )
			pmcidText = ''
				
			# Try to extract the publication date
			pubYear = 0
			if len(yearFields) > 0:
				pubYear = yearFields[0].text
			if len(medlineDateFields) > 0:
				pubYear = medlineDateFields[0].text[0:4]
				
			# Extract the title of paper
			title = elem.findall('./Article/ArticleTitle')
			titleText = extractTextFromElemList(title)
			titleText = [ removeWeirdBracketsFromOldTitles(t) for t in titleText ]
			
			# Extract the abstract from the paper
			abstract = elem.findall('./Article/Abstract/AbstractText')
			abstractText = extractTextFromElemList(abstract)
			
			# Combine all the text we want to process
			allText = titleText + abstractText
			allText = [ t for t in allText if len(t) > 0 ]
			allText = [ htmlUnescape(t) for t in allText ]
			allText = [ removeBracketsWithoutWords(t) for t in allText ]
			
			# Information about the source of this text
			textSourceInfo = {'pmid':pmidText, 'pmcid':pmcidText, 'pubYear':pubYear}
			
			# Get the co-occurrences using a single list
			processFunction(outFile, allText, textSourceInfo)
			
			# Important: clear the current element from memory to keep memory usage low
			elem.clear()
			
	
# Process a block of PubMed Central files
# Pass in the list of filenames, the mode to parse it with and whether to merge the output
def processArticleFiles(filelist, outFile, processFunction):
	if not isinstance(filelist, list):
		filelist = [filelist]

	# Go through the list of filenames and open each one
	for filename in filelist:
		with open(filename, 'r') as openfile:

			# Skip to the article element in the file
			for event, elem in etree.iterparse(openfile, events=('start', 'end', 'start-ns', 'end-ns')):
				if (event=='end' and elem.tag=='article'):
				
					# Attempt to extract the PubMed ID and PubMed Central IDs
					pmidText = ""
					pmcidText = ""
					article_id = elem.findall('./front/article-meta/article-id')
					for a in article_id:
						if a.text and "pub-id-type" in a.attrib and a.attrib["pub-id-type"] == "pmid":
							pmidText = a.text
						if a.text and "pub-id-type" in a.attrib and a.attrib["pub-id-type"] == "pmc":
							pmcidText = a.text
							
					# Attempt to get the publication date
					pubdates = elem.findall('./front/article-meta/pub-date')
					pubYear = ""
					for a in pubdates:
						pubYear = a.find("year").text
					
					# Extract the title of paper
					title = elem.findall('./front/article-meta/title-group/article-title')
					titleText = extractTextFromElemList(title)
					titleText = [ removeWeirdBracketsFromOldTitles(t) for t in titleText ]
					
					# Extract the abstract from the paper
					abstract = elem.findall('./front/article-meta/abstract')
					abstractText = extractTextFromElemList(abstract)
					
					# Extract the full text from the paper
					article = elem.findall('./body')
					articleText = extractTextFromElemList(article)
					
					# Combine all the text we want to process
					allText = titleText + abstractText + articleText
					allText = [ t for t in allText if len(t) > 0 ]
					allText = [ htmlUnescape(t) for t in allText ]
					allText = [ removeBracketsWithoutWords(t) for t in allText ]
					
					# Information about the source of this text
					textSourceInfo = {'pmid':pmidText, 'pmcid':pmcidText, 'pubYear':pubYear}
					
					# Get the co-occurrences using a single list
					processFunction(outFile, allText, textSourceInfo)
				
					# Less important here (compared to abstracts) as each article file is not too big
					elem.clear()

# Load a word-list file into a dictionary with IDs
# Allow removal of stopwords and short words
# Also can load directly from a pickled file or save to a pickled file		
def loadWordlistFile(wordlistPath, stopwordsFile, removeShortwords, binaryTermsFile, binaryTermsFile_out):
	wordlist = {}
	
	# Load the word-list directly from a pickled file
	if binaryTermsFile:
		# print "Loading idLookup1 from binary file:", binaryTermsFile.name
		wordlist = pickle.load(binaryTermsFile)
		print "Load complete."
	# Load a word-list from a file if needed
	elif os.path.isfile(wordlistPath):
		# Open the file with a unicode object
		f = codecs.open(wordlistPath, encoding='utf-8')
		
		duplicateList = []
		
		print "Loading terms list with synonyms..."
		# For each term, split it using the delimiter and insert it into the dictionary
		for (i,terms) in enumerate(f):
			for term in terms.split('|'):
				term = handleEncoding(term.strip().lower())
				key = tokenize(term)
				# Add it to the duplicate list if it already exists
				if key in wordlist:
					duplicateList.append(key)
				else:
					wordlist[key] = i
		print "Completed loading of " + str(len(wordlist)) + " terms."

		# Remove terms that appear more than once in a word-list
		print "Removing duplicate terms..."
		before = len(wordlist)
		for term in duplicateList:
			if term in wordlist:
				del wordlist[term]
		after = len(wordlist)
		print "Removed "+str(before-after)+" duplicate terms..."
			
		# Remove words from a set of stop-words, e.g. from the NLTK
		if stopwordsFile:
			print "Removing stopwords..."
			for stopword in stopwordsFile:
				stopword = tokenize(stopword)
				if stopword in wordlist:
					print "  Removing " + str(stopword) + " from termlist 1"
					del wordlist[stopword]
			print "Completed removal of stopwords"

		# Filter out words less than two characters long
		if removeShortwords:
			print "Removing short words..."
			before = len(wordlist)
			wordlist = {word:id for word,id in wordlist.iteritems() if sum(map(len,word)) > 2 }
			after = len(wordlist)
			print "Completed removal of " + str(before-after) + " short words"

	# Or save it to a pickled file
	if binaryTermsFile_out:
		print "Saving idLookup1 to binary file:", binaryTermsFile_out.name
		pickle.dump(wordlist, binaryTermsFile_out)
		print "Save complete."
		
	return wordlist
