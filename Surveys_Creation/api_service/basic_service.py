import requests # > 2.12.0

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

    def make_get_request(self, request_url):
        response = None
        for i in range(0, MAX_ATTEMPTS):
            response = self.client.get(request_url)
            if response:
                break

        return response.json()

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

    def get_pages_ids(self, survey_id):
        """ Return the ids of the pages in the survey """
        pages_info = self.get_pages_info(survey_id)
        page_ids = []
        for page in pages_info["data"]:
            page_ids.append(page["id"])
        return page_ids

    def add_page_description(self, survey_id, page_id, paragraph):
        """ Add description of the page """
        pass

    def add_paragraph(self, survey_id, page_id, abstract):
        """ Add a block of text to the page """
        url = HOST + "/surveys/%s/pages/%s/questions" % (survey_id, page_id)

        pass

    def add_question(self, survey_id, page_id, question):
        """ Add a question to the page """ 
        pass
