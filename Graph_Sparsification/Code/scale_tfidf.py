# Saling the tfidf values with a scaler
import argparse

def main():
    # Parse arguments
    args = parse_arguments()
    # Scale and sample
    scale_occurrences(args.t, args.s, args.out)

def parse_arguments():
    """ Parse argument inputs """
    parser = argparse.ArgumentParser(description='Scale all the tfidf values in the tfidf file')
    parser.add_argument('--t', type=str, help='Tfidf file')
    parser.add_argument('--s', type=int, help='Scalar by which to scale the tfidf values')
    parser.add_argument('--out', type=str, help="Folder to write the result to.")

    args = parser.parse_args()

    return args

def scale_occurrences(tfidf_file, scale, outfolder):
    """ Sample the tfidf values by scaling them and sample at various rates """
    outfile = "{0}/{1}_{2}".format(outfolder, tfidf_file.split("/")[-1], scale)

    with open(tfidf_file) as f, open(outfile, 'w') as out:
        for line in f:
            modifiedLine = ""
            if line != "\n":
                pairs = line.strip().split("\t")
                for p in pairs:
                    term, freq = p.split()
                    freq = int(round(float(freq) * scale, 0))
                    modifiedLine += (' '.join([term, str(freq)]) + '\t' )
            out.write(modifiedLine.strip() + "\n") # strip out the last tab and add the new line character

if __name__ == '__main__':
    main()
