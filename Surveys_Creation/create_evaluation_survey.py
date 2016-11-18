from api_service import basic_service
from private import appInfo


loremipsum = "Lorem ipsum dolor sit amet, consecteteur adipiscing elit donec proin nulla vivamus. Augue donec a erat ve sagittis nisi rhoncus curabitur mauris. Nulla ipsum tortor sagittis adipiscing primis interdum suspendisse lobortis etiam risus nullam. Donec massa quam dis at nibh dolor netus quis. Purus etiam. Dolor neque nunc netus eget nulla faucibus vestibulum aenean class senectus. Porta dolor. Donec morbi. Felis lorem tempus luctus malesuada laoreet curae justo rhoncus ante facilisi parturient malesuada elit laoreet amet. Fusce augue nisi ligula praesent condimentum nascetur fringilla in id lectus per nunc. Lacus metus nisl orci odio maecenas adipiscing. Velit nulla a tempor class placerat ac condimentum nisi taciti at eros."

client = basic_service.ApiService(appInfo.ACCESS_TOKEN)

#Create a new survey
# survey_id = client.create_survey("Evaluation_template")
# print(survey_id)
# # Create five pages of survey
# for i in range(0, 2):
#     print(client.create_new_page(survey_id, str(i), loremipsum)) # title and description
#     #print r.json()
#     print
# # Get the page ids
# ids = client.get_pages_ids(survey_id)
#
# print(ids)

page_ids = ["26984311", "26984312", "26984314"]
survey_id = "111307043"
answers = ["A", "B"]
question_title = "Which is more relevant?"
for ID in page_ids:
#    print(client.get_page_info(survey_id, ID))
#    print(client.update_title_description_of_page(survey_id, ID, "TITLE", loremipsum))
    print(client.add_single_choice(survey_id, ID, question_title, answers))
    print(client.add_paragraph(survey_id, ID, loremipsum))
    print(client.add_paragraph(survey_id, ID, loremipsum))

print
print(client.get_pages_info(survey_id))
