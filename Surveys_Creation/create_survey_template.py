from api_service import basic_service
from private import appInfo
import argparse
import time

def main():
    args = parseArgs()

    client = basic_service.ApiService(appInfo.ACCESS_TOKEN)
    survey_id = create_evaluation_template(client, args.name)

    print(survey_id)

def parseArgs():
    """ Parse the argument and do sanity check """
    parser = argparse.ArgumentParser(description='Create survey template' )
    parser.add_argument('--name', type=str, help='Name of the survey')
    args = parser.parse_args()

    return args

def create_evaluation_template(client, survey_name):
    """ Create a survey template """

    loremipsum = "Lorem ipsum dolor sit amet, consecteteur adipiscing elit donec proin nulla vivamus. Augue donec a erat ve sagittis nisi rhoncus curabitur mauris. Nulla ipsum tortor sagittis adipiscing primis interdum suspendisse lobortis etiam risus nullam. Donec massa quam dis at nibh dolor netus quis. Purus etiam. Dolor neque nunc netus eget nulla faucibus vestibulum aenean class senectus. Porta dolor. Donec morbi. Felis lorem tempus luctus malesuada laoreet curae justo rhoncus ante facilisi parturient malesuada elit laoreet amet. Fusce augue nisi ligula praesent condimentum nascetur fringilla in id lectus per nunc. Lacus metus nisl orci odio maecenas adipiscing. Velit nulla a tempor class placerat ac condimentum nisi taciti at eros."

    loremipsum_A = "A: \n" + loremipsum
    loremipsum_B = "B: \n" + loremipsum

    # Create a new survey
    survey_id = client.create_survey(survey_name)
    # Create 2 more pages in the survey
    for i in range(0, 2):
        client.create_new_page(survey_id, str(i), loremipsum) # title and description

    # Get the page ids
    page_ids = client.get_pages_ids(survey_id) # There will be 3

    answers = ["A", "B"]
    question_title = "Which of the following abstract is more relevant to the one above?"
    for i, ID in enumerate(page_ids):
        client.update_title_description_of_page(survey_id, ID, "Abstract" + str(i), loremipsum)
        client.add_single_choice(survey_id, ID, question_title, answers)
        client.add_paragraph(survey_id, ID, loremipsum_A)
        client.add_paragraph(survey_id, ID, loremipsum_B)

    return survey_id


if __name__ == '__main__':
    main()
