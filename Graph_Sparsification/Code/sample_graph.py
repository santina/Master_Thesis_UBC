import sys
import timeit
import argparse
import random


def main():
    # Parse the arguments
    parseArgs()
    # Sample the term frequencies in the file
    sampleAllOccurrences(args.f, args.out, args.rate)

def parseArgs():
    """ Parse the argument and do sanity check """
    parser = argparse.ArgumentParser(description='Sample a portion of the term-frequency matrix to simulate graph sparsification.')
    parser.add_argument('--f', type=str, help='term-frequency file')
    parser.add_argument('--out', type=str, help='Subsample of the term-frequency file')
    parser.add_argument('--rate', type=float, help="Sampling rate")
    args = parser.parse_args()

    if args.rate <= 0:
        print("Input has invalid rate")
        sys.exit()

    return args

def sample(freq, rate):
    """ Sample the frequency by applying a rate on each occurence """
    sampled_freq = 0
    for i in range(0, freq):
        sampled_freq += 1 if random.random() > (1-rate) else 0
    return sampled_freq

def sampleAllOccurrences(termFreqFile, outfile, rate):
    """ Sample the term frequency in the `termFreqFile` """
    with open(termFreqFile) as f, open(outfile, 'w') as out:
        for line in f:
            modifiedLine = ""
            if line != "\n":
                pairs = line.strip().split("\t")
                for p in pairs:
                    term, freq = p.split()
                    freq = sample(int(freq), rate)
                    if freq > 0:
                        modifiedLine += (' '.join([term, str(freq)]) + '\t' )
            out.write(modifiedLine.strip() + "\n") # strip out the last tab and add the new line character


if __name__ == '__main__':
	main()
