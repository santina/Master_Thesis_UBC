# Parse the log file output from running Graphlab into a format
# that can be more easily be read into an R table. On multiple files for TF, IDF, Binary

import argparse
from os import listdir
from os.path import isfile, isdir, join

def main():
    args = parse_args()
    write_summary(args.folder, args.out)

def parse_args():
    parser = argparse.ArgumentParser(description='Parse GraphLab singular value file into a R data frame')
    parser.add_argument('--folder', type=str, help='GraphLab output folder')
    parser.add_argument('--out', type=str, help='Outfile')

    # Folder > folders for each type (tf, tfidf, binary) > matrix folder

    args = parser.parse_args()
    return args

def write_summary(GraphLab_output_folder, out_file):
    """ Parse the log file into a tab delimited text file for creating R data.frame """
    out = open(out_file, "w")
    # Write header
    out.write("\t".join(["matrix_type", "matrix_name", "rank", "singular_value", "error_estimate"]) + '\n')

    for metric_folder in [f for f in listdir(GraphLab_output_folder) if isdir(join(GraphLab_output_folder, f))]:
        metric_name = metric_folder
        metric_folder = join(GraphLab_output_folder, metric_folder)


        # Obtain the log file for that folder of SVD outputs
        for matrix_folder in [f for f in listdir(metric_folder) if isdir(join(metric_folder, f))]:
            currFolder = join(metric_folder, matrix_folder)
            matrix_name = matrix_folder.replace(".matrix.svd", "")

            for f in [f for f in listdir(currFolder) if isfile(join(currFolder, f))]:
                if ".log" in f:
                    logfile = join(currFolder, f)

                    with open(logfile) as log:

                        for line in log:
                            if "Error estimate:" in line:
                                rank, sval, error = parse_line(line)
                                rank = str(int(rank) + 1 ) # First rank is 0 
                                out.write("\t".join([metric_name, matrix_name, rank, sval, error]) + '\n')


def parse_line(line):
    """ Parse the line with all three pieces of information about a singular value """
    line = line.split() # ['Singular', 'value', '1544', '658.074', 'Error', 'estimate:', '1.42256']
    return line[2], line[3], line[6]


if __name__ == '__main__':
    main()
