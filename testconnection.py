"""pymauro is an opensource library that wraps the REST API of Mauro Data Mapper instances in Python classes with
associated methods to allow easy, automated development.

Classes:

    BaseClient

Functions:
    test_my_url()

Currently documentation is lacking but the functionality can be approximately described by viewing the Java methods
as described in the documentation for the analogous Java Client library at
https://maurodatamapper.github.io/resources/client/java/#binding-vs-non-binding-clients """
import requests
import json

def test_my_url(url):
    """Takes the url (string) and appends /api/test.
This new path is then sent a get request. The response is
returned """
    response = requests.get(url + "/api/test")
    return response


class BaseClient:
    """
    A class to connect to a Mauro Data Mapper instance.

    """
    def __init__(self, baseurl, username, password, api_key=None):
        self.baseURL = baseurl
        self.username = username
        self.__password = password
        self.api_key = api_key
        if 'id' in self.test_my_connection().json().keys():
            self.cookie = self.test_my_connection().cookies
        if self.api_key is not None:
            self.headers = self.test_my_connection().headers
            self.headers['apiKey'] = self.api_key
        else:
            self.cookie = None

    def test_my_connection(self):
        json_payload = dict(username=self.username, password=self.__password)
        response = requests.post(self.baseURL + "/api/authentication/login", json=json_payload)
        return response

    def check_for_valid_session(self):
        response = requests.get(self.baseURL + "/api/session/isAuthenticated", cookies=self.cookie)
        return response

    def logout(self):
        response = requests.get(self.baseURL + "/api/authentication/logout", cookies=self.cookie)
        return response

    def admin_check(self):
        if self.api_key is not None:
            response = requests.get(self.baseURL + "/api/session/isApplicationAdministration",
                                    headers={'apiKey': self.api_key})
            return response
        else:
            return "API Key must be provided"

    def __repr__(self):
        return "Mauro Client Object"

    def list_apis(self, id=None):
        if self.api_key is not None:
            default_id=self.test_my_connection().json()['id']
            if id is None:
                response = requests.get(self.baseURL + "/api/catalogueUsers/" + str(default_id) + "/apiKeys",
                                        headers={'apiKey': self.api_key})
            else:
                response = requests.get(self.baseURL + "/api/catalogueUsers/" + id + "/apiKeys",
                                        headers={'apiKey': self.api_key})
            return response

        else:
            return "API Key must be provided"


    def create_new_api_key(self, key_name='My Name', expiry=365, refreshable=True, id=None, ):
        if self.api_key is not None:
            default_id=self.test_my_connection().json()['id']
            json_payload = dict(name=key_name, expiresInDays=expiry,refreshable=refreshable)
            if id is None:
                response = requests.post(self.baseURL + "/api/catalogueUsers/" + str(default_id) + "/apiKeys",
                                        headers={'apiKey': self.api_key}, json=json_payload)
            else:
                response = requests.post(self.baseURL + "/api/catalogueUsers/" + id + "/apiKeys",
                                        headers={'apiKey': self.api_key}, json=json_payload)
            return response

        else:
            return "API Key must be provided"



    def delete_api_key(self, key_to_delete, id=None):
        if self.api_key is not None:
            default_id=self.test_my_connection().json()['id']
            if id is None:
                response = requests.delete(self.baseURL + "/api/catalogueUsers/" + str(default_id) + "/apiKeys/" + str(key_to_delete),
                                        headers={'apiKey': self.api_key})
            else:
                response = requests.delete(self.baseURL + "/api/catalogueUsers/" + id + "/apiKeys/" + str(key_to_delete) ,
                                        headers={'apiKey': self.api_key})
            return response

        else:
            return "API Key must be provided"


    def disable_api_key(self, key_to_disable, id=None):
        if self.api_key is not None:
            default_id=self.test_my_connection().json()['id']
            if id is None:
                response = requests.put(self.baseURL + "/api/catalogueUsers/" + str(default_id) + "/apiKeys/"
                                        + str(key_to_disable) +"/disable",headers={'apiKey': self.api_key})
            else:
                response = requests.put(self.baseURL + "/api/catalogueUsers/" + id + "/apiKeys/" + str(key_to_disable)
                                        +"/disable",headers={'apiKey': self.api_key})
            return response

        else:
            return "API Key must be provided"

    def enable_api_key(self, key_to_disable, id=None):
        if self.api_key is not None:
            default_id=self.test_my_connection().json()['id']
            if id is None:
                response = requests.put(self.baseURL + "/api/catalogueUsers/" + str(default_id) + "/apiKeys/"
                                        + str(key_to_disable) +"/enable",headers={'apiKey': self.api_key})
            else:
                response = requests.put(self.baseURL + "/api/catalogueUsers/" + id + "/apiKeys/" + str(key_to_disable)
                                        +"/enable",headers={'apiKey': self.api_key})
            return response

        else:
            return "API Key must be provided"

    def refresh_api_key(self, key_to_disable, days_until_expiry, id=None):
        if self.api_key is not None:
            default_id=self.test_my_connection().json()['id']
            if id is None:
                response = requests.put(self.baseURL + "/api/catalogueUsers/" + str(default_id) + "/apiKeys/"
                                        + str(key_to_disable) +"/refresh/" + str(days_until_expiry),headers={'apiKey': self.api_key})
            else:
                response = requests.put(self.baseURL + "/api/catalogueUsers/" + id + "/apiKeys/" + str(key_to_disable)
                                        +"/refresh/" + str(days_until_expiry),headers={'apiKey': self.api_key})
            return response

        else:
            return "API Key must be provided"



    def list_folders(self, offset=0, max=10, all=False):
        if all == False:
            response = requests.get(self.baseURL + "/api/folders?offset="+str(offset)+"&max="+str(max), headers={'apiKey': self.api_key})
        else:
            response = requests.get(self.baseURL + "/api/folders?all=true", headers={'apiKey': self.api_key})
        return response





MyClient = BaseClient("https://modelcatalogue.cs.ox.ac.uk/ons", "thomas.heneghan@ons.gov.uk", "Dredds1996!",
                      api_key="5eb00202-3701-47ca-9bda-317e209b29ee")


# print(MyClient.admin_check().json())
# print(test_my_url.__doc__)






