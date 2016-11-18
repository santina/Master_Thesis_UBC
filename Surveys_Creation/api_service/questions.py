# A factory that provides dictionary object used in making Survey Monkey question.

PARAGRAPH = {
    "headings": [
        {
            "heading": ""
        }
    ],
    "family": "presentation",
    "subtype": "descriptive_text"
}

SINGLE_CHOICE = {
    "headings": [
        {
            "heading": ""
        }
    ],
    "family": "single_choice",
    "subtype": "vertical",
    "answers": {
        "choices":[
        ]
    }
}

"""
    @input : a list of strings representing the choice text
    @output: a dictionary with correct schema for survey monkey
"""
def _format_text_choices(choice_list):
    choice_schema = []
    for choice in choice_list:
        choice_schema.append(
            {
                "text": choice
            }
        )
    return choice_schema


'''
    @input:
        question : a string
        choices : a list of strings for difference choices
        position (optional) : 1-base index, position of the question in the survey, default to be placed last
    @output:
        a dictionary form of a single-choice question for Survey Monkey
'''
def make_single_choice_question(question_title, choices, position=None):
    question = SINGLE_CHOICE.copy()
    question["headings"][0]["heading"] = question_title

    question["answers"]["choices"] = _format_text_choices(choices)
    if position:
        question["position"] = position
    return question

'''
    @input:
        question: a string
        position (optional) : 1-base index, position of the question in the survey, default to be placed last
    @output:
        a dictionary form of a block of text for Survey Monkey
'''
def make_paragraph(paragraph_text, position=None):
    question = PARAGRAPH.copy()
    question["headings"][0]["heading"] = paragraph_text
    if position:
        question["position"] = position
    return question
