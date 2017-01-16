from api_service import basic_service
from private import appInfo
import argparse
import time
from collections import defaultdict

# Obtain the responses from a survey given a survey ID. Record the choice ids
# for each question and each response to a file. If there are multiple responses
# to the survey, the choices ids are concatenated in one line 

def main():
    # Parse the arguments
    args = parseArgs()
    client = basic_service.ApiService(appInfo.ACCESS_TOKEN)
    responses = get_responses(client, args.id)
    choices = parse_responses(responses)
    record_responses(choices, args.out)

def parseArgs():
    parser = argparse.ArgumentParser(description='Obtain and record survey responses')
    parser.add_argument('--id', type=str, help="Survey ID")
    parser.add_argument('--out', type=str, help="File for storing the resposnes")
    args = parser.parse_args()

    return args

def get_responses(client, survey_id):
    responses = client.get_surve_responses(survey_id)
    return responses["data"]

def parse_responses(responses):
    choices = defaultdict(list)
    # typically there should only be one response, but in case there are more than 1
    for response in responses:
        questions = response["pages"][1:] # omit the contact page
        question_num = 1
        for question in questions:
            # We want the first question (only 1 exist, the other two are abstracts A and B)
            # and we want the first answer (there's only 1 because it's multiple choice)
            choice_id = question["questions"][0]["answers"][0]["choice_id"]
            choices[question_num].append(choice_id)
            question_num += 1
    return choices

def record_responses(choices, outfile):
    out = open(outfile, "w")
    for i in range(1,len(choices) + 1):
        choice_ids = ' '.join(choices[i])
        out.write(choice_ids + '\n')
    out.close()

if __name__ == '__main__':
    main()
