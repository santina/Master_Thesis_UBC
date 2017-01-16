from . import questions
import requests

# Survey Monkey host.
HOST = "https://api.surveymonkey.net/v3"

# Maximum number of attempts to get a successful response.
MAX_ATTEMPTS = 5

"""
    This API service focuses on creation of surveys and getting the survey details and details about their pages
"""

class ApiService(object):
    def __init__(self, access_token):
        self.client = requests.session()
        self.client.headers = {
            "Authorization": "bearer %s" % access_token,
            "Content-Type": "application/json"
        }

    def make_post_request(self, request_url, payload):
        response = None
        for i in range(0,MAX_ATTEMPTS):
            response = self.client.post(request_url, json=payload)
            if response:
                break

        return response.json()

    def make_put_request(self, request_url, payload):
        response = None
        for i in range(0,MAX_ATTEMPTS):
            response = self.client.put(request_url, json=payload)
            if response:
                break

        return response.json()

    def make_get_request(self, request_url):
        response = None
        for i in range(0, MAX_ATTEMPTS):
            response = self.client.get(request_url)
            if response:
                break

        return response.json()

    def get_surveys(self):
        """ Returns a list of surveys owned or shared with the authenticated user. """
        url = HOST + "/surveys"

        response = self.make_get_request(url)
        return response

    def create_survey(self, survey_name):
        """ Create an empty survey given the name and return the survey ID """
        url = HOST + "/surveys"
        payload = {
            "title" : survey_name
        }
        response = self.make_post_request(url, payload)

        return response["id"]

    def clone_survey(self, survey_name, template_id):
        """ Create a survey by cloning an existing template and return the
        the survey ID """

        url = HOST + "/surveys"
        payload = {
            "title" : survey_name,
            "from_survey_id" : str(template_id)
        }
        response = self.make_post_request(url, payload)

        return response["id"]

    def get_survey_info(self, survey_id):
        """ Obtain information about a survey
        https://developer.surveymonkey.com/api/v3/?python#surveys-id
        """
        url = HOST + "/surveys/%s" %(survey_id)
        return self.make_get_request(url)

    def get_pages_info(self, survey_id):
        """ Obtain information about the pages in a survey """
        url = HOST + "/surveys/%s/pages" %(survey_id)
        return self.make_get_request(url)

    def get_page_info(self, survey_id, page_id):
        """ Obtain information for one specific page in a survey """
        url = HOST + "/surveys/%s/pages/%s" %(survey_id, page_id)
        return self.make_get_request(url)

    def get_pages_ids(self, survey_id):
        """ Return the ids of the pages in the survey """
        pages_info = self.get_pages_info(survey_id)
        page_ids = []
        for page in pages_info["data"]:
            page_ids.append(page["id"])
        return page_ids

    def get_questions_ids(self, survey_id, page_id):
        url = HOST + "/surveys/%s/pages/%s/questions" %(survey_id, page_id)
        response =  self.make_get_request(url)
        questions_ids = []
        for question in response["data"]:
            questions_ids.append(question["id"])
        return questions_ids

    def get_survey_link(self, survey_id):
        """ Get the link to the survey at which people can do the survey """
        url = HOST + "/surveys/%s/collectors" %(survey_id)
        payload = {
            "type": "weblink"
        }
        response = self.make_post_request(url, payload)
        return response["url"]

    def get_survey_details(self, survey_id):
        url  = HOST + "/surveys/%s/details" % (survey_id)
        responses = self.make_get_request(url)
        return responses

    def create_new_page(self, survey_id, title, description):
        """ Create a new page with title and description of the page,
        and return the page id """
        url = HOST + "/surveys/%s/pages" % (survey_id)
        payload = {
          "title": title,
          "description" : description
        }
        response = self.make_post_request(url, payload)
        return response

    def update_title_description_of_page(self, survey_id, page_id, title, description):
        """ Modify the title and description of a page in a survey. """
        url = HOST + "/surveys/%s/pages/%s" %(survey_id, page_id)
        payload = {
          "title": title,
          "description" : description
        }
        response = self.make_put_request(url, payload)
        return response

    def add_paragraph(self, survey_id, page_id, text):
        """ Add a block of text to the page. """
        url = HOST + "/surveys/%s/pages/%s/questions" % (survey_id, page_id)
        text_data = questions.make_paragraph(text)
        response = self.make_post_request(url, text_data)
        return response

    def add_single_choice(self, survey_id, page_id, title, choices):
        """ Add a single_choice question to the page """
        url = HOST + "/surveys/%s/pages/%s/questions" % (survey_id, page_id)
        question_data = questions.make_single_choice_question(title, choices)
        response = self.make_post_request(url, question_data)
        return response

    def add_paragraph_with_random_placement(self, survey_id, page_id, text, positions, probs):
        url = HOST + "/surveys/%s/pages/%s/questions" % (survey_id, page_id)
        text_data = questions.make_paragraph(text)
        text_data["headings"] = questions.add_random_placement(text_data, positions, probs)
        print(text_data)
        print
        response = self.make_post_request(url, text_data)
        return response

    def replace_single_choice_question(self, survey_id, page_id, question_id, title, choices):
        url = HOST + "/surveys/%s/pages/%s/questions/%s" % (survey_id, page_id, question_id)
        question_data = questions.make_single_choice_question(title, choices)
        response = self.make_put_request(url, question_data)

    def replace_paragraph_text(self, survey_id, page_id, question_id, text):
        url = HOST + "/surveys/%s/pages/%s/questions/%s" % (survey_id, page_id, question_id)
        text_data = questions.make_paragraph(text)
        response = self.make_put_request(url, text_data)
