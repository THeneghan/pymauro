#Named pymauro
import requests

class BaseClient:
    def __init__(self,baseURL,username,password):
        self.baseURL=baseURL
        self.username=username
        self.password=password
        if 'id' in self.test_my_connection().json().keys():
            self.cookie=self.test_my_connection().cookies


    def test_my_connection(self):
        json_payload={}
        json_payload['username']=self.username
        json_payload['password']=self.password
        response = requests.post(self.baseURL+"/api/authentication/login", json=json_payload)
        return response

    def check_for_valid_session(self):
        response=requests.get(self.baseURL+"/api/session/isAuthenticated",cookies=self.cookie)
        return response




def test_my_url(url):
    response = requests.get(url + "/api/test")
    return response

MyClient = BaseClient("https://modelcatalogue.cs.ox.ac.uk/ons","thomas.heneghan@ons.gov.uk","Dredds1996!")
#print(MyClient.test_connection().json())
MyClient.check_for_valid_session()
print(MyClient.check_for_valid_session().json())




