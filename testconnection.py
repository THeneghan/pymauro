#Named pymauro
import requests
import json
from requests.auth import HTTPBasicAuth


class BaseClient:
    def __init__(self, baseurl, username, password, api_key=None):
        self.baseURL = baseurl
        self.username = username
        self.__password = password
        self.api_key=api_key
        if 'id' in self.test_my_connection().json().keys():
            self.cookie = self.test_my_connection().cookies
        if self.api_key is not None:
            self.headers=self.test_my_connection().headers
            print(type(self.headers))
            self.headers['apiKey']=self.api_key
            self.newy={'apiKey':self.api_key}
            print(self.headers)

        else:
            self.cookie = None

    def test_my_connection(self):
        json_payload = dict(username=self.username, password=self.__password)
        response = requests.post(self.baseURL+"/api/authentication/login", json=json_payload)
        return response

    def check_for_valid_session(self):
        response = requests.get(self.baseURL+"/api/session/isAuthenticated", cookies=self.cookie)
        return response

    def logout(self):
        response = requests.get(self.baseURL+"/api/authentication/logout", cookies=self.cookie)
        return response



    def admin_check(self):
        if self.api_key is not None:
            response = requests.get(self.baseURL+"/api/session/isApplicationAdministration", headers={'apiKey':self.api_key})
            return response


    def __repr__(self):
        if self.check_for_valid_session().json()['authenticatedSession']:
            return F"Mauro Client Object: Logged in as {self.username} @ {self.baseURL}"
        else:
            return "Mauro Client Object: Not logged in"

    # def list_existing_api_keys(self):
    #     response=requests.get(self.baseURL+"/api/catalogueUsers/logout")


def test_my_url(url):
    response = requests.get(url + "/api/test")
    return response


MyClient = BaseClient("https://modelcatalogue.cs.ox.ac.uk/ons", "thomas.heneghan@ons.gov.uk", "Dredds1996!",api_key=
                      "5eb00202-3701-47ca-9bda-317e209b29ee")
print(MyClient.admin_check().json())

