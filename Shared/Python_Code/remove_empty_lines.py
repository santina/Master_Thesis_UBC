# Three tasks:
## Remove empty lines from the tf file -> input for GraphLab
## Create a new abstract list that do not include abstracts that have no matching terms
## Create an abstract list that do not have matching terms, for sanity checking

# Rationale: missing lines in the final decomposed matrix poses a problem for the cosine similarity function
import argparse

def main():
    args = read_args()
    remove_empty_lines(args.tf, args.tfout, args.abstract, args.abstract1, args.abstract0, args.log)

def read_args():
    parser = argparse.ArgumentParser(description='Remove empty lines')
    parser.add_argument('--tf', type=str, help='term-frequency file')
    parser.add_argument('--tfout', type=str, help='term-frequency file with no empty lines')
    parser.add_argument('--abstract', type=str, help="abstract file")
    parser.add_argument('--abstract1', type=str, help="new abstract file with no empty lines")
    parser.add_argument('--abstract0', type=str, help="abstract file with remaining abstract")
    parser.add_argument('--log', type=str, help="log file recording the removed line numbers")
    args = parser.parse_args()

    return args

def remove_empty_lines(tf, tf_out, abstracts, abstract_out, abstract_excluded, log):
    tf_new = open(tf_out, "w")
    abstract_new = open(abstract_out, "w")
    abstract_removed = open(abstract_excluded, "w")
    log_out = open(log, "w")

    i = 1
    # Read the term frequency file and the abstract file together
    with open(tf) as t, open(abstracts) as ab:
        for tf_line, ab_line in zip(t, ab):
            if tf_line != "\n":
                abstract_new.write(ab_line)
                tf_new.write(tf_line)
            else:
                abstract_removed.write(ab_line)
                log_out.write(str(i) + "\n")
            i += 1



if __name__ == '__main__':
    main()
