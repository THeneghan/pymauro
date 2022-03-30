import config
import testconnection as tc

#Fine
MyClient = tc.BaseClient("https://modelcatalogue.cs.ox.ac.uk/ons", "thomas.heneghan@ons.gov.uk", config.password,
                         api_key="5eb00202-3701-47ca-9bda-317e209b29ee")
#Fine
MyClient2 = tc.BaseClient("https://modelcatalogue.cs.ox.ac.uk/ons", api_key="5eb00202-3701-47ca-9bda-317e209b29ee")

#Fine
MyClient3 = tc.BaseClient("https://modelcatalogue.cs.ox.ac.uk/ons", "thomas.heneghan@ons.gov.uk", config.password)

#Doesn't work, don't know why
#tc.test_my_url("https://modelcatalogue.cs.ox.ac.uk/ons")

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

#print(MyClient3.list_apis("a43c5618-e660-4fdf-af3a-8c7528b58982").json())
#print(MyClient3.list_apis().json())


#print(MyClient3.list_apis("a43c5618-e660-4fdf-af3a-8c7528b58982").json())
#print(MyClient2.test_my_connection())



#Fails as you need to use session identifier for this endpoint (gives appropriate error message)


# print(MyClient.properties("folders","3b3ca080-0c75-4a50-a993-5ec6e87f631e").json())
