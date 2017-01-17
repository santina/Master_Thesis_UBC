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

    # If there is at least one response, record the data
    if int(responses["total"]) > 0:
        record_responses(responses, args.responses)
        record_contact(responses, args.contact)

def parseArgs():
    parser = argparse.ArgumentParser(description='Obtain and record survey responses')
    parser.add_argument('--id', type=str, help="Survey ID")
    parser.add_argument('--responses', type=str, help="File for storing the resposnes")
    parser.add_argument('--contact', type=str, help="File for storing the contact information")
    args = parser.parse_args()

    return args

def get_responses(client, survey_id):
    responses = client.get_surve_responses(survey_id)
    return responses

def record_responses(responses, outfile):
    data = responses["data"]
    out = open(outfile, "w")
    # typically there should only be one response, but in case there are more than 1
    for response in data:
        questions = response["pages"][1:] # omit the contact page
        choices = []
        for question in questions:
            # We want the first question (only 1 exist, the other two are abstracts A and B)
            # and we want the first answer (there's only 1 because it's multiple choice)
            try:
                choice_id = question["questions"][0]["answers"][0]["choice_id"]
            except IndexError:
                choice_id = "---------"
            choices.append(choice_id)

        out.write(' '.join(choices) + '\n')
    return choices

def record_contact(responses, outfile):
    data = responses["data"]
    out = open(outfile, "w")
    for response in data:
        contact_page = response["pages"][0]  # First page
        answer = contact_page["questions"][0]["answers"] # only one question
        try:
            contact_info = '\t'.join([ answer[0]["text"], answer[1]["text"] ]) # name and email
        except:
            contact_info = contact_page["questions"][0]
        out.write(str(contact_info) + '\n')

if __name__ == '__main__':
    main()
