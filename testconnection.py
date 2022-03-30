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

    It is recommended that you provide both a username/password and api key as some methods only operate off the
    provision of one and not the other.

    The user must provide at least a username and password or an API key. A type error will return if the arguments
    provided are not valid

    """

    def __init__(self, baseurl, username=None, password=None, api_key=None):
        self.baseURL = baseurl
        self.username = username
        self.__password = password
        self.api_key = api_key
        if (self.username is None or self.__password is None) and self.api_key is None \
                or self.username is not None and self.__password is None \
                or self.username is None and self.__password is not None:
            raise TypeError("You must provide at a minimum: the username and password as a pairing or an API Key.")
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
        if self.username is None:
            raise TypeError("You must provide a username and password to access this method")
        response = requests.get(self.baseURL + "/api/authentication/logout", cookies=self.cookie)
        return response

    def admin_check(self):
        if self.api_key is not None:
            response = requests.get(self.baseURL + "/api/session/isApplicationAdministration",
                                    headers={'apiKey': self.api_key})
        else:
            response = requests.get(self.baseURL + "/api/session/isApplicationAdministration",
                                    cookies=self.cookie)
        return response

    def __repr__(self):
        return "Mauro Client Object"

    def list_apis(self, id_input=None):
        if self.username is None and id_input is None:
            raise TypeError("A username/password or an id "
                            "method argument is required for this method to work")
        elif self.api_key is None and id_input is None:
            default_id = self.test_my_connection().json()['id']
            response = requests.get(self.baseURL + "/api/catalogueUsers/" + default_id + "/apiKeys",
                                    cookies=self.cookie)
            return response
        elif self.api_key is None and id_input is not None:
            response = requests.get(self.baseURL + "/api/catalogueUsers/" + id_input + "/apiKeys",
                                    cookies=self.cookie)
            return response
        elif self.api_key is not None and id_input is None:
            default_id = self.test_my_connection().json()['id']
            response = requests.get(self.baseURL + "/api/catalogueUsers/" + str(default_id) + "/apiKeys",
                                    headers={'apiKey': self.api_key})
            return response
        elif self.api_key is not None and id_input is not None:
            response = requests.get(self.baseURL + "/api/catalogueUsers/" + id_input + "/apiKeys",
                                    headers={'apiKey': self.api_key})
            return response

    def create_new_api_key(self, key_name='My Name', expiry=365, refreshable=True, id_input=None, ):
        if self.api_key is not None:
            default_id = self.test_my_connection().json()['id']
            json_payload = dict(name=key_name, expiresInDays=expiry, refreshable=refreshable)
            if id_input is None:
                response = requests.post(self.baseURL + "/api/catalogueUsers/" + str(default_id) + "/apiKeys",
                                         headers={'apiKey': self.api_key}, json=json_payload)
            else:
                response = requests.post(self.baseURL + "/api/catalogueUsers/" + id_input + "/apiKeys",
                                         headers={'apiKey': self.api_key}, json=json_payload)
            return response
        else:
            raise TypeError("An API Key must be passed to this instance of class for this method to work")

    def delete_api_key(self, key_to_delete, id_input=None):
        if self.api_key is not None:
            default_id = self.test_my_connection().json()['id']
            if id_input is None:
                response = requests.delete(
                    self.baseURL + "/api/catalogueUsers/" + str(default_id) + "/apiKeys/" + str(key_to_delete),
                    headers={'apiKey': self.api_key})
            else:
                response = requests.delete(
                    self.baseURL + "/api/catalogueUsers/" + id_input + "/apiKeys/" + str(key_to_delete),
                    headers={'apiKey': self.api_key})
            return response
        else:
            raise TypeError("An API Key must be passed to this instance of class for this method to work")

    def disable_api_key(self, key_to_disable, id_input=None):
        if self.api_key is not None:
            default_id = self.test_my_connection().json()['id']
            if id_input is None:
                response = requests.put(self.baseURL + "/api/catalogueUsers/" + str(default_id) + "/apiKeys/"
                                        + str(key_to_disable) + "/disable", headers={'apiKey': self.api_key})
            else:
                response = requests.put(self.baseURL + "/api/catalogueUsers/" + id_input + "/apiKeys/"
                                        + str(key_to_disable) + "/disable", headers={'apiKey': self.api_key})
            return response
        else:
            raise TypeError("An API Key must be passed to this instance of class for this method to work")

    def enable_api_key(self, key_to_disable, id_input=None):
        if self.api_key is not None:
            default_id = self.test_my_connection().json()['id']
            if id_input is None:
                response = requests.put(self.baseURL + "/api/catalogueUsers/" + str(default_id) + "/apiKeys/"
                                        + str(key_to_disable) + "/enable", headers={'apiKey': self.api_key})
            else:
                response = requests.put(self.baseURL + "/api/catalogueUsers/" + id_input + "/apiKeys/" +
                                        str(key_to_disable) + "/enable", headers={'apiKey': self.api_key})
            return response

        else:
            raise TypeError("An API Key must be passed to this instance of class for this method to work")

    def refresh_api_key(self, key_to_disable, days_until_expiry, id_input=None):
        if self.api_key is not None:
            default_id = self.test_my_connection().json()['id']
            if id_input is None:
                response = requests.put(self.baseURL + "/api/catalogueUsers/" + str(default_id) + "/apiKeys/"
                                        + str(key_to_disable) + "/refresh/" + str(days_until_expiry),
                                        headers={'apiKey': self.api_key})
            else:
                response = requests.put(self.baseURL + "/api/catalogueUsers/" + id_input + "/apiKeys/" +
                                        str(key_to_disable) + "/refresh/" + str(days_until_expiry),
                                        headers={'apiKey': self.api_key})
            return response
        else:
            raise TypeError("An API Key must be passed to this instance of class for this method to work")

    def list_folders(self, offset=0, max_limit=10, show_all=False):
        if self.api_key is not None:
            if not show_all:
                response = requests.get(self.baseURL + "/api/folders?offset=" + str(offset) + "&max=" + str(max_limit),
                                        headers={'apiKey': self.api_key})
            else:
                response = requests.get(self.baseURL + "/api/folders?all=true", headers={'apiKey': self.api_key})

        else:
            if not show_all:
                response = requests.get(self.baseURL + "/api/folders?offset=" + str(offset) + "&max=" + str(max_limit),
                                        cookies=self.cookie)
            else:
                response = requests.get(self.baseURL + "/api/folders?all=true", cookies=self.cookie)
        return response

    def properties(self, catalogue_item_domain_type, catalogue_item_id):
        if self.api_key is not None:
            val_domain_types = ["folders", "dataModels", "dataClasses", "dataTypes", "terminologies", "terms",
                                "referenceDataModels"]
            if catalogue_item_domain_type not in val_domain_types:
                return "catalogueItemDomainType must be in " + str(val_domain_types)
            response = requests.get(
                self.baseURL + "/api/" + str(catalogue_item_domain_type) + "/" + str(catalogue_item_id) + "/metadata",
                headers={'apiKey': self.api_key})
            return response
        else:
            raise TypeError("An API Key must be passed to this instance of class for this method to work")

    def permissions(self, catalogue_item_domain_type, id_input):
        val_domain_types = ["folders", "dataModels", "dataClasses", "dataTypes", "terminologies", "terms",
                            "referenceDataModels"]
        if catalogue_item_domain_type not in val_domain_types:
            return "catalogueItemDomainType must be in " + str(val_domain_types)
        print(self.baseURL + "/api/" + str(catalogue_item_domain_type) + "/" + str(id_input) + "/permissions")
        print(self.cookie)
        response = requests.get(self.baseURL + "/api/" + str(catalogue_item_domain_type) + "/" + str(id_input) +
                                "/permissions", cookies=self.cookie)
        return response

    def post_metadata(self, catalogue_item_domain_type, catalogue_item_id, namespace_inp, key_val, value_inp):
        val_domain_types = ["folders", "dataModels", "dataClasses", "dataTypes", "terminologies", "terms",
                            "referenceDataModels"]
        if catalogue_item_domain_type not in val_domain_types:
            return "catalogueItemDomainType must be in " + str(val_domain_types)
        json_payload = dict(id=catalogue_item_id, namespace=namespace_inp, key=key_val, value=value_inp)
        response = requests.post(
            self.baseURL + "/api/" + str(catalogue_item_domain_type) + "/" + str(catalogue_item_id) + "/metadata",
            headers={'apiKey': self.api_key}, json=json_payload)
        return response
