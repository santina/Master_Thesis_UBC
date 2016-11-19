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
        question: formatted question schema for survey monkey
        position list: a list of integers specifying the position change
        probabilities : a list of integer (must add up to 100) for chances of placement
    @output:
        a modified question schema
'''
def add_random_placement(question, position_list, probabilities):
        # check inputs
    if len(position_list) != len(probabilities):
        print( "Cannot assign random placement due to bad inputs")
        return
    if sum(probabilities) != 100:
        print("Cannot assign placement due to bad probability list")
        return
        
    headings = []
    question_title = question["headings"][0]["heading"]
    for i in range(0, len(position_list)):
        headings.append(
            {
                "random_assignment": {
                    "position": position_list[i],
                    "percent": probabilities[i]
                },
                "heading": question_title
            }
        )

    return headings

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
