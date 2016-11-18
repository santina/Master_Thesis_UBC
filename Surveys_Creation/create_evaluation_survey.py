from api_service import basic_service
from private import appInfo

client = basic_service.ApiService(appInfo.ACCESS_TOKEN)
#print(client.get_pages_ids(111171813))
#print(client.clone_survey("Test4.1", 111171813))
print(client.create_survey("Test5"))
