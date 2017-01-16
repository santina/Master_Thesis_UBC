# Purpose

This folder contains all the Python code needed to do the surveys to test whether PubMed or SVD perform better. 


## api_services
- Contains the class with all the essential functions to make post and get requests, used by the Python scripts

## private
- Not uploaded onto GitHub. Contains the access token and client ID of my draft app

# stand-alone Python scripts

- create_data.py
    - takes input from the `find_ranks.sh` in the big matrix bash scripts folder
    - make calls to Entrez.Bio to get the title and abstract text for each pmid
    - Output input data to `create_evaluation_survey.py`
    - data are in the form of:  
```
    {
        "target": {
            "ID": ... ,
            "abstract": ... ,
            "title":  ...,
            "choice" : ""
            },
        "pubmed": {
            "ID": ... ,
            "abstract": ... ,
            "title":  ...,
            "choice" : "<1 or 2>"
            },
        "svd": {
            "ID": ... ,
            "abstract": ... ,
            "title":  ...,
            "choice" : "<1 or 2>"
            },  
    }
```
- create_evaluation_survey.py
    - Given the name, input data, create a survey and store important information about the survey in two files
        - tab-delimited output file: survey ID, survey link
        - choice IDs for each question. The file has three column and each line is for a question.
            - Column 1 : choice A
            - Column 2 : choice B
            - Column 3 : Both are equally relevant/irrelevant.

- obtain_survey_responses.py
    - Given a survey ID, output the response data in the form of choice IDs of the choices that people have selected
    - Format of the output file (space-delimited, each line is a separate response to the survey):
        choice ID for question 1, choice ID for question 2, ....
        - Skipped question will have answer in the form of "---------"
    - Also record the contact of the respondant.

- do_choice_counts.py
    - Given the output from obtain_survey_responses.py, do a tally by mapping the IDs to the actual svd/pubmed choice
