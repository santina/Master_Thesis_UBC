# Parse the log file output from running Graphlab into a format
# that can be more easily be read into an R table.
# header : rank  singluar_value  error_estimate

import argparse

def main():
    args = parse_args()
    write_summary(args.log, args.out)

def parse_args():
    parser = argparse.ArgumentParser(description='Parse GraphLab singular value file into a R data frame')
    parser.add_argument('--log', type=str, help='GraphLab output file')
    parser.add_argument('--out', type=str, help='Outfile')

    args = parser.parse_args()
    return args

def write_summary(singular_file, out_file):
    """ Parse the log file into a tab delimited text file for creating R data.frame """
    with open(singular_file) as f, open(out_file, "w") as out:
        # Write header
        out.write("\t".join(["rank", "singular_value", "error_estimate"]) + '\n')

        for line in f:
            if "Error estimate:" in line:
                rank, sval, error = parse_line(line)
                data = map(str, [rank, sval, error])
                out.write("\t".join(data) + '\n')


def parse_line(line):
    """ Parse the line with all three pieces of information about a singular value """
    line = line.split() # ['Singular', 'value', '1544', '658.074', 'Error', 'estimate:', '1.42256']
    return line[2], line[3], line[6]


if __name__ == '__main__':
    main()
