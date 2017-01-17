import argparse
from collections import defaultdict

# this simple python script does a count of how many choices are
# SVD, PubMed or neither


def main():
    args = parseArgs()
    chart = make_lookup_chart(args.ids)
    svd_or_pubmed = make_svd_pubmed_lookup(args.abstracts)
    summarize(args.responses, chart, svd_or_pubmed, args.out)

def parseArgs():
    parser = argparse.ArgumentParser(description='Obtain and record survey responses')
    parser.add_argument('--responses', type=str, help="File with the response data from obtain_survey_responses.py")
    parser.add_argument('--ids', type=str, help="File with choice ids data from create_evaluation_survey.py")
    parser.add_argument('--abstracts', type=str, help="File with abstracts that create the survey (from create_data.py)")
    parser.add_argument('--out', type=str, help="File for recording count data")
    args = parser.parse_args()

    # Note: choice 1 is denoted as choice A, and 2 is B. Each choice in each answer has a different ID assigned by Survey Monkey.

    return args

def make_lookup_chart(ids_file):
    chart = []
    f = open(ids_file)
    for i, ids in enumerate(f):
        ids = ids.strip().split()
        chart.append({
            ids[0] : "A",
            ids[1] : "B",
            ids[2] : "C" # The neither choice
        })
    return chart

def make_svd_pubmed_lookup(abstracts_file):
    chart = []
    for line in open(abstracts_file):
        data = eval(line)
        chart.append({
            "A": "svd" if data["svd"]["choice"] == 1 else "pubmed",
            "B": "svd" if data["svd"]["choice"] == 2 else "pubmed",
            "C": "neither"
        })
    return chart

def summarize(responses_file, id_chart, svd_or_pubmed, outfile):
    out = open(outfile, "w")
    result = []
    for i, line in enumerate(open(responses_file)):
        line = line.strip().split()
        abstract_types = []
        for j, ID in enumerate(line):
            abstract_type = look_up(ID, j, id_chart, svd_or_pubmed)
            abstract_types.append(abstract_type)
        result.append(abstract_types)

    # write to file
    total = tally(result)
    out.write('\t'.join( map(str, total) ) + '\n')
    for line in result:
        out.write( '\t'.join( line ) + '\n' )


def look_up(ID, line_num, id_chart, svd_or_pubmed):
    try:
        choice = id_chart[line_num][ID]
        abstract_type = svd_or_pubmed[line_num][choice]
        return abstract_type
    except:
        return "-----"

def tally(result):
    tallied_result = [0, 0, 0]  # pubmed, svd, neither
    for line in result:
        tallied_result[0] += line.count("pubmed")
        tallied_result[1] += line.count("svd")
        tallied_result[2] += line.count("neither")

    return tallied_result

if __name__ == '__main__':
    main()
