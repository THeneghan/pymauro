import config
import testconnection as tc

#All should instantiate fine
MyClient = tc.BaseClient("https://modelcatalogue.cs.ox.ac.uk/ons", "thomas.heneghan@ons.gov.uk", config.password,
                         api_key="5eb00202-3701-47ca-9bda-317e209b29ee")
MyClient2 = tc.BaseClient("https://modelcatalogue.cs.ox.ac.uk/ons", api_key="5eb00202-3701-47ca-9bda-317e209b29ee")

MyClient3 = tc.BaseClient("https://modelcatalogue.cs.ox.ac.uk/ons", "thomas.heneghan@ons.gov.uk", config.password)


#Fails as incomplete password/username pairing is given
#FailingClient = tc.BaseClient("https://modelcatalogue.cs.ox.ac.uk/ons", password="val",api_key="5eb00202-3701-47ca-9bda-317e209b29ee")

#Fails as neither API key or password/username is given
#FailingClient2 = tc.BaseClient("https://modelcatalogue.cs.ox.ac.uk/ons")


#Fails (raises TypeError) as needs username and password for json payload
#MyClient2.test_my_connection()
#MyClient2.check_for_valid_session()
#MyClient2.logout()



#Fine as username/password provided
#MyClient.test_my_connection()
#MyClient3.test_my_connection()
#MyClient3.check_for_valid_session()
#MyClient3.logout()

#Fine as method can use either session id or api key but prioritises API Key (useful for longer jobs where is may logout)
# print(MyClient3.admin_check().json())
# print(MyClient.admin_check().json())
# print(MyClient2.admin_check().json())

#Quite complicated but shows how arguments provided change method procedure
#print(MyClient.list_apis("a43c5618-e660-4fdf-af3a-8c7528b58982").json())
#print(MyClient.list_apis().json())
#print(MyClient2.list_apis("a43c5618-e660-4fdf-af3a-8c7528b58982").json())

#Fails as no api key provided and no input provided
#print(MyClient2.list_apis().json())


#print(MyClient.create_new_api_key("hello5").json())
#print(MyClient3.create_new_api_key("hello6").json())

#print(MyClient2.create_new_api_key("hello2").json())

#print(MyClient3.delete_api_key("ffa27c47-ed37-46ef-9c68-55d8600e355f","a43c5618-e660-4fdf-af3a-8c7528b58982").json())
#print(MyClient.delete_api_key("hello55",id_input="a43c5618-e660-4fdf-af3a-8c7528b58982").json())
#print(MyClient3.delete_api_key("hello65",id_input="a43c5618-e660-4fdf-af3a-8c7528b58982").json())

#print(MyClient2.refresh_api_key("3015b2ce-4f7c-4265-9f14-88710379f24e",10,"a43c5618-e660-4fdf-af3a-8c7528b58982").json())


#print(MyClient.get_classifer().json())

print(MyClient.get_classifers().json())
print(MyClient2.get_classifers().json())
print(MyClient3.get_classifers().json())

MyClient.get_data

#print(MyClient3.get_data_classes("c2e3034d-f127-4130-9224-26641ab3b0de").json())
#print(MyClient.get_data_element("654c255a-c54d-405b-b8da-7ca0c7193f35","ac1519c6-0f9f-4a06-b198-69a508a9cacb").json())






#Need to do properties etc onwards

#print(MyClient3.list_apis("a43c5618-e660-4fdf-af3a-8c7528b58982").json())
#print(MyClient3.list_apis().json())


#print(MyClient3.list_apis("a43c5618-e660-4fdf-af3a-8c7528b58982").json())
#print(MyClient2.test_my_connection())



#Fails as you need to use session identifier for this endpoint (gives appropriate error message)


# print(MyClient.properties("folders","3b3ca080-0c75-4a50-a993-5ec6e87f631e").json())

