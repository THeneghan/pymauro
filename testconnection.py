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

    It is recommended that you provide both a password and api key as some methods only operate off the provision of
    one and not the other

    """

    def __init__(self, baseurl, username=None, password=None, api_key=None):
        self.baseURL = baseurl
        self.username = username
        self.__password = password
        self.api_key = api_key
        if self.api_key is None and self.username is None or self.api_key is None and self.__password is None\
                or self.username is not None and self.__password is None \
                or self.username is None and self.__password is not None:
            raise TypeError("You must provide at a minimum: the username and password or an API Key.")
        if self.api_key is not None:
            self.headers = dict()
            self.headers['apiKey'] = self.api_key
        if self.username is not None and 'id' in self.test_my_connection().json().keys():
            self.cookie = self.test_my_connection().cookies
        else:
            self.cookie = None


    def test_my_connection(self):
        if self.username is None:
            raise TypeError("You must provide a username and password to access this method")
        json_payload = dict(username=self.username, password=self.__password)
        response = requests.post(self.baseURL + "/api/authentication/login", json=json_payload)
        return response

    def check_for_valid_session(self):
        if self.username is None:
            raise TypeError("You must provide a username and password to access this method")
        response = requests.get(self.baseURL + "/api/session/isAuthenticated", cookies=self.cookie)
        return response

    def logout(self):
        if self.username is None or self.__password is None:
            raise TypeError("You must provide a username and password to access this method")
        response = requests.get(self.baseURL + "/api/authentication/logout", cookies=self.cookie)
        return response

    def admin_check(self):
        if self.api_key is not None:
            response = requests.get(self.baseURL + "/api/session/isApplicationAdministration",
                                    headers={'apiKey': self.api_key})
            return response
        else:
            raise TypeError("An API Key must be passed to this instance of class for this method to work")

    def __repr__(self):
        return "Mauro Client Object"

    def list_apis(self, id=None):
        if self.api_key is not None:
            default_id = self.test_my_connection().json()['id']
            if id is None:
                response = requests.get(self.baseURL + "/api/catalogueUsers/" + str(default_id) + "/apiKeys",
                                        headers={'apiKey': self.api_key})
            else:
                response = requests.get(self.baseURL + "/api/catalogueUsers/" + id + "/apiKeys",
                                        headers={'apiKey': self.api_key})
            return response

        else:
            raise TypeError("An API Key must be passed to this instance of class for this method to work")

    def create_new_api_key(self, key_name='My Name', expiry=365, refreshable=True, id=None, ):
        if self.api_key is not None:
            default_id = self.test_my_connection().json()['id']
            json_payload = dict(name=key_name, expiresInDays=expiry, refreshable=refreshable)
            if id is None:
                response = requests.post(self.baseURL + "/api/catalogueUsers/" + str(default_id) + "/apiKeys",
                                         headers={'apiKey': self.api_key}, json=json_payload)
            else:
                response = requests.post(self.baseURL + "/api/catalogueUsers/" + id + "/apiKeys",
                                         headers={'apiKey': self.api_key}, json=json_payload)
            return response
        else:
            raise TypeError("An API Key must be passed to this instance of class for this method to work")

    def delete_api_key(self, key_to_delete, id=None):
        if self.api_key is not None:
            default_id = self.test_my_connection().json()['id']
            if id is None:
                response = requests.delete(
                    self.baseURL + "/api/catalogueUsers/" + str(default_id) + "/apiKeys/" + str(key_to_delete),
                    headers={'apiKey': self.api_key})
            else:
                response = requests.delete(
                    self.baseURL + "/api/catalogueUsers/" + id + "/apiKeys/" + str(key_to_delete),
                    headers={'apiKey': self.api_key})
            return response
        else:
            raise TypeError("An API Key must be passed to this instance of class for this method to work")

    def disable_api_key(self, key_to_disable, id=None):
        if self.api_key is not None:
            default_id = self.test_my_connection().json()['id']
            if id is None:
                response = requests.put(self.baseURL + "/api/catalogueUsers/" + str(default_id) + "/apiKeys/"
                                        + str(key_to_disable) + "/disable", headers={'apiKey': self.api_key})
            else:
                response = requests.put(self.baseURL + "/api/catalogueUsers/" + id + "/apiKeys/" + str(key_to_disable)
                                        + "/disable", headers={'apiKey': self.api_key})
            return response
        else:
            raise TypeError("An API Key must be passed to this instance of class for this method to work")

    def enable_api_key(self, key_to_disable, id=None):
        if self.api_key is not None:
            default_id = self.test_my_connection().json()['id']
            if id is None:
                response = requests.put(self.baseURL + "/api/catalogueUsers/" + str(default_id) + "/apiKeys/"
                                        + str(key_to_disable) + "/enable", headers={'apiKey': self.api_key})
            else:
                response = requests.put(self.baseURL + "/api/catalogueUsers/" + id + "/apiKeys/" + str(key_to_disable)
                                        + "/enable", headers={'apiKey': self.api_key})
            return response

        else:
            raise TypeError("An API Key must be passed to this instance of class for this method to work")

    def refresh_api_key(self, key_to_disable, days_until_expiry, id=None):
        if self.api_key is not None:
            default_id = self.test_my_connection().json()['id']
            if id is None:
                response = requests.put(self.baseURL + "/api/catalogueUsers/" + str(default_id) + "/apiKeys/"
                                        + str(key_to_disable) + "/refresh/" + str(days_until_expiry),
                                        headers={'apiKey': self.api_key})
            else:
                response = requests.put(self.baseURL + "/api/catalogueUsers/" + id + "/apiKeys/" + str(key_to_disable)
                                        + "/refresh/" + str(days_until_expiry), headers={'apiKey': self.api_key})
            return response
        else:
            raise TypeError("An API Key must be passed to this instance of class for this method to work")

    def list_folders(self, offset=0, max=10, all=False):
        if self.api_key is not None:
            if not all:
                response = requests.get(self.baseURL + "/api/folders?offset=" + str(offset) + "&max=" + str(max),
                                        headers={'apiKey': self.api_key})
            else:
                response = requests.get(self.baseURL + "/api/folders?all=true", headers={'apiKey': self.api_key})

        else:
            if not all:
                response = requests.get(self.baseURL + "/api/folders?offset=" + str(offset) + "&max=" + str(max),
                                        cookies=self.cookie)
            else:
                response = requests.get(self.baseURL + "/api/folders?all=true", cookies=self.cookie)
        return response


    def properties(self, catalogueItemDomainType, catalogueItemId):
        if self.api_key is not None:
            val_domain_types= ["folders","dataModels","dataClasses","dataTypes","terminologies","terms","referenceDataModels"]
            if catalogueItemDomainType not in val_domain_types:
                return "catalogueItemDomainType must be in " + str(val_domain_types)
            response = requests.get(self.baseURL + "/api/" + str(catalogueItemDomainType) +"/" + str(catalogueItemId) +"/metadata", headers={'apiKey': self.api_key})
            return response
        else:
            raise TypeError("An API Key must be passed to this instance of class for this method to work")



    def permissions(self,catalogueItemDomainType, id):
        val_domain_types= ["folders","dataModels","dataClasses","dataTypes","terminologies","terms","referenceDataModels"]
        if catalogueItemDomainType not in val_domain_types:
            return "catalogueItemDomainType must be in " + str(val_domain_types)
        print(self.baseURL + "/api/" + str(catalogueItemDomainType)+"/" + str(id) +"/permissions")
        print(self.cookie)
        response = requests.get(self.baseURL + "/api/" + str(catalogueItemDomainType)+"/" + str(id) +"/permissions", cookies=self.cookie)
        return response

    def post_metadata(self, catalogueItemDomainType, catalogueItemId, namespace_inp, key_val, value_inp):
        val_domain_types = ["folders", "dataModels", "dataClasses", "dataTypes", "terminologies", "terms",
                            "referenceDataModels"]
        if catalogueItemDomainType not in val_domain_types:
            return "catalogueItemDomainType must be in " + str(val_domain_types)
        json_payload = dict(id=catalogueItemId,namespace=namespace_inp,key=key_val,value=value_inp)
        response = requests.post(
            self.baseURL + "/api/" + str(catalogueItemDomainType) + "/" + str(catalogueItemId) + "/metadata",
            headers={'apiKey': self.api_key}, json=json_payload)
        return response






