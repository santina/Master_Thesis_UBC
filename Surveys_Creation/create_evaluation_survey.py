from api_service import basic_service
from private import appInfo
import argparse
import time

def main():
    args = parseArgs()

    # Initialize the template ID and the client for creating a new survey
    template_ID = 111307043
    client = basic_service.ApiService(appInfo.ACCESS_TOKEN)

    # Make the survey and save the survey link
    survey_id = create_survey_from_questions(client, template_ID, args.name, args.f)
    store_choice_info(client, survey_id, args.choiceInfo)
    store_survey_link(client, survey_id, args.name, args.linkInfo)

    # NOTE: Each survey creation makes 32 API calls. Limited to 120 calls/minute
    # and 500 calls/day. So you can only make maximum of 16 surveys a day.

def parseArgs():
    """ Parse the argument and do sanity check """
    parser = argparse.ArgumentParser(description='Create a survey with a template' )
    parser.add_argument('--f', type=str, help='question file')
    parser.add_argument('--name', type=str, help='Name of the survey')
    parser.add_argument('--linkInfo', type=str, help="File to store the survey link")
    parser.add_argument('--choiceInfo', type=str, help="File to store the choice IDs so we know which IDs refer to which choice (A or B)")
    args = parser.parse_args()

    return args

def create_survey_from_questions(client, template_ID, survey_name, question_file):
    """ Iterate through the file and create a question for each line """
    survey_id = clone_survey(client, survey_name, template_ID)
    page_ids = get_survey_page_ids(client, survey_id) # This will return a list of page IDs

    # Index of page_ids. Starts at 1 to omit the first page (contact info)
    page_index = 1

    for question in open(question_file):
        question = eval(question) # make the string into a dictionary
        print(question["svd"]["choice"])
        change_survey_page(client, question, survey_id, page_ids[page_index])
        page_index += 1
        if page_index > len(page_ids) - 1:  # in case I have too many questions
            break

    return survey_id

def change_survey_page(client, question, survey_id, page_id):

    change_target_abstract(client, question, survey_id, page_id)
    change_AB_abstracts(client, question, survey_id, page_id)

def change_target_abstract(client, question, survey_id, page_id):
    target = make_abstract_paragraph(question, "target")
    # Modify the target abstract
    modify_survey_page_target_abstract(client, survey_id, page_id, "", target)

def change_AB_abstracts(client, question, survey_id, page_id):
    # Get the question ids
    questions_ids = client.get_questions_ids( survey_id, page_id )

    # Modify the abstract
    modify_abstract(client, survey_id, page_id, questions_ids, question, "svd")
    modify_abstract(client, survey_id, page_id, questions_ids, question, "pubmed")

def make_abstract_paragraph(question, abstract_type):
    return "TITLE: %s \n ABSTRACT: %s " %(question[abstract_type]["title"], question[abstract_type]["abstract"])

def store_choice_info(client, survey_id, outfile):
    survey_detail = client.get_survey_details(survey_id)
    survey_detail = survey_detail["pages"]

    out = open(outfile, "w")
    for page in survey_detail[1:]:
        question = page["questions"][0]["answers"]["choices"]
        choice_A_id = question[0]["id"]
        choice_B_id = question[1]["id"]
        choice_C_id = question[2]["id"]
        out.write(choice_A_id + '\t' + choice_B_id + '\t' + choice_C_id + '\n')
    out.close()

def store_survey_link(client, survey_id, survey_name, outfile):
    """ Get the survey link and store it in the file """
    survey_link = client.get_survey_link(survey_id)
    out = open(outfile, "w")
    out.write(str(survey_id) + '\t' + survey_name + '\t' + survey_link + '\n')
    out.close()

def get_surveys(client):
    return client.get_surveys()

def get_survey_page_ids(client, survey_id):
    result = client.get_pages_ids(survey_id)
    return result

def get_page_question_ids(client, survey_id, page_ids):
    """ Return the question ids in a given page. In our use case, there should be 3 : one for the question itself, and two for the two abstract paragraphs. """

    return client.get_pages_ids(survey_id, page_ids)

def clone_survey(client, survey_name, template_id):
    """ Make a copy of a survey given the survey id """
    clone_id = client.clone_survey(survey_name, template_id)
    return clone_id

def modify_survey_page_target_abstract(client, survey_id, page_id, new_title, target_abstract):
    """ Modify the target abstract text of a page in a survey """
    response = client.update_title_description_of_page(survey_id, page_id, new_title, target_abstract)
    return response

def modify_question_text(client, survey_id, page_id, question_id, abstract_pmid):
    """ Modify the question """
    title = "Which of the following abstracts are closest to abstract " + str(abstract_pmid)
    answers = ["A", "B"]
    response = client.replace_single_choice_question(survey_id, page_id, question_id, title, answers)
    return response

def modify_abstract(client, survey_id, page_id, questions_ids, question, abstract_type):
    """ Change the A or B abstract """  # TODO: make the A / B more distinguishable
    # obtain choice
    choice = int(question[abstract_type]["choice"])
    text = make_abstract_paragraph(question, abstract_type)

    if choice == 1:
        text = "A: \n" + text
    else:
        text = "B: \n" + text
    client.replace_paragraph_text(survey_id, page_id, questions_ids[choice], text)


if __name__ == '__main__':
    main()
