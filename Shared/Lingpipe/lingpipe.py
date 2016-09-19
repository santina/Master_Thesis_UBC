import subprocess
#import xml.dom.minidom
import time

class LingPipe:
	path = ''
	def __init__(self, pathToLingPipe):
		self.path = pathToLingPipe
		self.process = subprocess.Popen([self.path],stdout=subprocess.PIPE,stdin=subprocess.PIPE)
	
	def parse(self, text):
		results = list()

		text = text.strip()
		if len(text) == 0:
			return results

		#print text
		#print str(self.process)
		for oneline in text.split('\n'):
			self.process.stdin.write(oneline+'\n')
			#print oneline
			while True:
				#print "HERE"
				r = self.process.stdout.readline()[:-1]
				#print r
				if not r:
					# Waiting for a blank line
					break
				results.append(r)
		return results

