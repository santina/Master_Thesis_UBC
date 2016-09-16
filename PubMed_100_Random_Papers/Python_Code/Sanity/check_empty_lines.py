import argparse 

def getEmptyLines(filename, outfile):
	empty_lines = list()

	with open(filename) as f, open(outfile, 'w') as out:
		for lineNum, line in enumerate(f): # 0 base for lineNum 
			if line.strip():
				continue
			else:
				empty_lines.append(lineNum)
		for l in empty_lines:
			out.write(str(l) + '\n')
	print len(empty_lines)

def printEmptyLines(filename):
	empty_lines = list()

	with open(filename) as f:
		for lineNum, line in enumerate(f): # 0 base for lineNum 
			if line.strip():
				continue
			else:
				empty_lines.append(lineNum)
	print empty_lines
	#print len(empty_lines)


def countEmptyLines(filename):
	count = 0
	with open(filename) as f:
		for lineNum, line in enumerate(f): # 0 base for lineNum 
			if line.strip():
				continue
			else:
				count += 1
	return count 

def hasEmptyLine(filename):
	if countEmptyLines(filename) > 0:
		return True
	return False 

def main():

	parser = argparse.ArgumentParser(description='Check or count empty lines')
	parser.add_argument('--f', type=str, help='input file')
	args = parser.parse_args()

	print hasEmptyLine(args.f)
	print countEmptyLines(args.f)
	printEmptyLines(args.f)

if __name__ == '__main__':
	main()