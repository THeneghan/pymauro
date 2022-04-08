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


def test_my_url(url):
    """Takes the url (string) and appends /api/test.
This new path is then sent a get request. The response is
returned

Arguments:
    url: A string
Returns:
    The get response for the url appended with /api/test"""
    response = requests.get(url + "/api/test")
    return response


class BaseClient:
    """
    A class to connect to a Mauro Data Mapper instance.

    It is recommended that you provide both a username/password and api key as some methods only operate off the
    provision of one and not the other.

    The user must provide at least a username and password or an API key. A type error will return if the arguments
    provided do not abide by this rule

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
        """Executes a post request with username and password as json payload to the baseurl appended with
        /api/authentication/login. The response is returned
        Arguments:
            None
        Returns:
            The post response for the url appended with /api/authentication/login"""
        if self.username is None:
            raise TypeError("You must provide a username and password to access this method")
        json_payload = dict(username=self.username, password=self.__password)
        response = requests.post(self.baseURL + "/api/authentication/login", json=json_payload)
        return response

    def check_for_valid_session(self):
        """Executes a get request to the url + /api/session/isAuthenticated
        with the session ID in the cookies header.
        The response is returned
        Arguments:
            None
        Returns:
            The get response for the url appended with /api/session/isAuthenticated"""
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
        response = None
        if self.username is None and id_input is None:
            raise TypeError("A username/password or an id "
                            "method argument is required for this method to work")
        elif self.api_key is None and id_input is None:
            default_id = self.test_my_connection().json()['id']
            response = requests.get(self.baseURL + "/api/catalogueUsers/" + default_id + "/apiKeys",
                                    cookies=self.cookie)
        elif self.api_key is None and id_input is not None:
            response = requests.get(self.baseURL + "/api/catalogueUsers/" + id_input + "/apiKeys",
                                    cookies=self.cookie)
        elif self.api_key is not None and id_input is None:
            default_id = self.test_my_connection().json()['id']
            response = requests.get(self.baseURL + "/api/catalogueUsers/" + str(default_id) + "/apiKeys",
                                    headers={'apiKey': self.api_key})
        elif self.api_key is not None and id_input is not None:
            response = requests.get(self.baseURL + "/api/catalogueUsers/" + id_input + "/apiKeys",
                                    headers={'apiKey': self.api_key})
        return response

    def create_new_api_key(self, key_name='My Name', expiry=365, refreshable=True, id_input=None):
        if self.username is None and id_input is None:
            raise TypeError("A username/password or an id "
                            "method argument is required for this method to work")
        elif self.api_key is not None:
            json_payload = dict(name=key_name, expiresInDays=expiry, refreshable=refreshable)
            if id_input is None:
                default_id = self.test_my_connection().json()['id']
                response = requests.post(self.baseURL + "/api/catalogueUsers/" + str(default_id) + "/apiKeys",
                                         headers={'apiKey': self.api_key}, json=json_payload)
            else:
                response = requests.post(self.baseURL + "/api/catalogueUsers/" + id_input + "/apiKeys",
                                         headers={'apiKey': self.api_key}, json=json_payload)
        else:
            if id_input is None:
                json_payload = dict(name=key_name, expiresInDays=expiry, refreshable=refreshable)
                default_id = self.test_my_connection().json()['id']
                response = requests.post(self.baseURL + "/api/catalogueUsers/" + str(default_id) + "/apiKeys",
                                         cookies=self.cookie, json=json_payload)
            else:
                json_payload = dict(name=key_name, expiresInDays=expiry, refreshable=refreshable)
                response = requests.post(self.baseURL + "/api/catalogueUsers/" + str(id_input) + "/apiKeys",
                                         cookies=self.cookie, json=json_payload)
        return response

    def delete_api_key(self, key_to_delete, id_input=None):
        if self.username is None and id_input is None:
            raise TypeError("A username/password or an id "
                            "method argument is required for this method to work")
        elif self.api_key is not None:
            if id_input is None:
                default_id = self.test_my_connection().json()['id']
                response = requests.delete(
                    self.baseURL + "/api/catalogueUsers/" + str(default_id) + "/apiKeys/" + str(key_to_delete),
                    headers={'apiKey': self.api_key})
            else:
                response = requests.delete(
                    self.baseURL + "/api/catalogueUsers/" + id_input + "/apiKeys/" + str(key_to_delete),
                    headers={'apiKey': self.api_key})
            return response
        else:
            if id_input is None:
                default_id = self.test_my_connection().json()['id']
                print(default_id)
                response = requests.delete(
                    self.baseURL + "/api/catalogueUsers/" + str(default_id) + "/apiKeys/" + str(key_to_delete),
                    cookies=self.cookie)
            else:
                response = requests.delete(
                    self.baseURL + "/api/catalogueUsers/" + id_input + "/apiKeys/" + str(key_to_delete),
                    cookies=self.cookie)
            return response

    def disable_api_key(self, key_to_disable, id_input=None):
        if self.username is None and id_input is None:
            raise TypeError("A username/password or an id "
                            "method argument is required for this method to work")
        elif self.api_key is not None:
            if id_input is None:
                default_id = self.test_my_connection().json()['id']
                response = requests.put(self.baseURL + "/api/catalogueUsers/" + str(default_id) + "/apiKeys/"
                                        + str(key_to_disable) + "/disable", headers={'apiKey': self.api_key})
            else:
                response = requests.put(self.baseURL + "/api/catalogueUsers/" + id_input + "/apiKeys/"
                                        + str(key_to_disable) + "/disable", headers={'apiKey': self.api_key})
            return response
        else:
            if id_input is None:
                default_id = self.test_my_connection().json()['id']
                response = requests.put(self.baseURL + "/api/catalogueUsers/" + str(default_id) + "/apiKeys/"
                                        + str(key_to_disable) + "/disable", cookies=self.cookie)
            else:
                response = requests.put(self.baseURL + "/api/catalogueUsers/" + id_input + "/apiKeys/"
                                        + str(key_to_disable) + "/disable", cookies=self.cookie)
            return response

    def enable_api_key(self, key_to_disable, id_input=None):
        if self.username is None and id_input is None:
            raise TypeError("A username/password or an id "
                            "method argument is required for this method to work")
        elif self.api_key is not None:
            if id_input is None:
                default_id = self.test_my_connection().json()['id']
                response = requests.put(self.baseURL + "/api/catalogueUsers/" + str(default_id) + "/apiKeys/"
                                        + str(key_to_disable) + "/enable", headers={'apiKey': self.api_key})
            else:
                response = requests.put(self.baseURL + "/api/catalogueUsers/" + id_input + "/apiKeys/" +
                                        str(key_to_disable) + "/enable", headers={'apiKey': self.api_key})
            return response

        else:
            if id_input is None:
                default_id = self.test_my_connection().json()['id']
                response = requests.put(self.baseURL + "/api/catalogueUsers/" + str(default_id) + "/apiKeys/"
                                        + str(key_to_disable) + "/enable", cookies=self.cookie)
            else:
                response = requests.put(self.baseURL + "/api/catalogueUsers/" + id_input + "/apiKeys/" +
                                        str(key_to_disable) + "/enable", cookies=self.cookie)
            return response

    def refresh_api_key(self, key_to_refresh, days_until_expiry, id_input=None):
        if self.username is None and id_input is None:
            raise TypeError("A username/password or an id "
                            "method argument is required for this method to work")
        elif self.api_key is not None:
            if id_input is None:
                default_id = self.test_my_connection().json()['id']
                response = requests.put(self.baseURL + "/api/catalogueUsers/" + str(default_id) + "/apiKeys/"
                                        + str(key_to_refresh) + "/refresh/" + str(days_until_expiry),
                                        headers={'apiKey': self.api_key})
            else:
                response = requests.put(self.baseURL + "/api/catalogueUsers/" + id_input + "/apiKeys/" +
                                        str(key_to_refresh) + "/refresh/" + str(days_until_expiry),
                                        headers={'apiKey': self.api_key})
            return response
        else:
            if id_input is None:
                default_id = self.test_my_connection().json()['id']
                response = requests.put(self.baseURL + "/api/catalogueUsers/" + str(default_id) + "/apiKeys/"
                                        + str(key_to_refresh) + "/refresh/" + str(days_until_expiry),
                                        cookies=self.cookie)
            else:
                response = requests.put(self.baseURL + "/api/catalogueUsers/" + id_input + "/apiKeys/" +
                                        str(key_to_refresh) + "/refresh/" + str(days_until_expiry),
                                        cookies=self.cookie)
            return response

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

    def get_metadata(self, catalogue_item_domain_type, catalogue_item_id, metadata_id=None):
        val_domain_types = ["folders", "dataModels", "dataClasses", "dataTypes", "terminologies", "terms",
                            "referenceDataModels"]
        if catalogue_item_domain_type not in val_domain_types:
            raise ValueError("catalogueItemDomainType must be in " + str(val_domain_types))
        if self.api_key is not None:
            if metadata_id is None:
                response = requests.get(
                    self.baseURL + "/api/" + str(catalogue_item_domain_type) + "/" + str(
                        catalogue_item_id) + "/metadata",
                    headers={'apiKey': self.api_key})
            else:
                response = requests.get(
                    self.baseURL + "/api/" + str(catalogue_item_domain_type) + "/" + str(
                        catalogue_item_id) + "/metadata/" + str(metadata_id),
                    headers={'apiKey': self.api_key})
            return response
        else:
            if metadata_id is None:
                response = requests.get(
                    self.baseURL + "/api/" + str(catalogue_item_domain_type) + "/" + str(
                        catalogue_item_id) + "/metadata",
                    cookies=self.cookie)
            else:
                response = requests.get(
                    self.baseURL + "/api/" + str(catalogue_item_domain_type) + "/" + str(
                        catalogue_item_id) + "/metadata/" + str(metadata_id),
                    cookies=self.cookie)
            return response

    def permissions(self, catalogue_item_domain_type, id_input):
        val_domain_types = ["folders", "dataModels", "dataClasses", "dataTypes", "terminologies", "terms",
                            "referenceDataModels"]
        if catalogue_item_domain_type not in val_domain_types:
            raise ValueError("catalogueItemDomainType must be in " + str(val_domain_types))
        if self.api_key is not None:
            response = requests.get(self.baseURL + "/api/" + str(catalogue_item_domain_type) + "/" + str(id_input) +
                                    "/permissions", headers={'apiKey': self.api_key})
            return response
        else:
            response = requests.get(self.baseURL + "/api/" + str(catalogue_item_domain_type) + "/" + str(id_input) +
                                    "/permissions", cookies=self.cookie)
            return response

    def post_metadata(self, catalogue_item_domain_type, catalogue_item_id, namespace_inp, key_val, value_inp):
        val_domain_types = ["folders", "dataModels", "dataClasses", "dataTypes", "terminologies", "terms",
                            "referenceDataModels"]
        if catalogue_item_domain_type not in val_domain_types:
            raise ValueError("catalogueItemDomainType must be in " + str(val_domain_types))
        json_payload = dict(id=catalogue_item_id, namespace=namespace_inp, key=key_val, value=value_inp)
        if self.api_key is not None:
            response = requests.post(
                self.baseURL + "/api/" + str(catalogue_item_domain_type) + "/" + str(catalogue_item_id) + "/metadata",
                headers={'apiKey': self.api_key}, json=json_payload)
            return response
        else:
            response = requests.post(
                self.baseURL + "/api/" + str(catalogue_item_domain_type) + "/" + str(catalogue_item_id) + "/metadata",
                cookies=self.cookie, json=json_payload)
            return response

    # def edit_metadata(self,catalogue_item_domain_type, catalogue_item_id,metadata_id, id_value):
    #     val_domain_types = ["folders", "dataModels", "dataClasses", "dataTypes", "terminologies", "terms",
    #                         "referenceDataModels"]
    #     if catalogue_item_domain_type not in val_domain_types:
    #         raise ValueError("catalogueItemDomainType must be in " + str(val_domain_types))
    #     json_payload = dict(metadata_id=id_value)
    #     if self.api_key is not None:
    #         response = requests.put(
    #             self.baseURL + "/api/" + str(catalogue_item_domain_type) + "/" + str(catalogue_item_id) + "/metadata/"
    #             + str(metadata_id),
    #             headers={'apiKey': self.api_key}, json=json_payload)
    #         return response
    #     else:
    #         response = requests.put(
    #             self.baseURL + "/api/" + str(catalogue_item_domain_type) + "/" + str(catalogue_item_id) + "/metadata/"
    #             + str(metadata_id),
    #             cookies=self.cookie, json=json_payload)
    #         return response

    def get_classifers(self, classifier_id=None, id_input=None):
        if self.api_key is not None:
            if classifier_id is None and id_input is None:
                response = requests.get(
                    self.baseURL + "/api/classifiers",
                    headers={'apiKey': self.api_key})
            elif classifier_id and id_input is None:
                response = requests.get(
                    self.baseURL + "/api/classifiers/" + str(classifier_id) + "/classifiers",
                    headers={'apiKey': self.api_key})
            elif id_input and classifier_id is None:
                response = requests.get(
                    self.baseURL + "/api/classifiers/" + str(id_input),
                    headers={'apiKey': self.api_key})
            elif id_input and id_input:
                response = requests.get(
                    self.baseURL + "/api/classifiers/" + str(classifier_id) + "/classifiers/" + str(id_input),
                    headers={'apiKey': self.api_key})
        else:
            if classifier_id is None and id_input is None:
                response = requests.get(
                    self.baseURL + "/api/classifiers",
                    cookies=self.cookie)
            elif classifier_id and id_input is None:
                response = requests.get(
                    self.baseURL + "/api/classifiers/" + str(classifier_id) + "/classifiers",
                    cookies=self.cookie)
            elif id_input and classifier_id is None:
                response = requests.get(
                    self.baseURL + "/api/classifiers/" + str(id_input),
                    cookies=self.cookie)
            elif id_input and id_input:
                response = requests.get(
                    self.baseURL + "/api/classifiers/" + str(classifier_id) + "/classifiers/" + str(id_input),
                    cookies=self.cookie)
        return response

    def get_data_classes(self, data_model_id, data_class_id=None, id_input=None):
        if self.api_key is not None:
            if data_class_id is None and id_input is None:
                response = requests.get(
                    self.baseURL + "/api/dataModels/" + str(data_model_id) + "/dataClasses",
                    headers={'apiKey': self.api_key})
            elif data_class_id and id_input is None:
                response = requests.get(
                    self.baseURL + "/api/dataModels/" + str(data_model_id) + "/dataClasses/" + str(data_class_id)
                    + "/dataClasses",
                    headers={'apiKey': self.api_key})
            elif id_input and data_class_id is None:
                response = requests.get(
                    self.baseURL + "/api/dataModels/" + data_model_id + "/dataClasses/" + str(id_input),
                    headers={'apiKey': self.api_key})
            elif id_input and id_input:
                response = requests.get(
                    self.baseURL + "/api/dataModels/" + str(data_model_id) + "/dataClasses/" + str(data_class_id) +
                    "/dataClasses/" + str(id_input),
                    headers={'apiKey': self.api_key})
        else:
            if data_class_id is None and id_input is None:
                response = requests.get(
                    self.baseURL + "/api/dataModels/" + str(data_model_id) + "/dataClasses",
                    cookies=self.cookie)
            elif data_class_id and id_input is None:
                response = requests.get(
                    self.baseURL + "/api/dataModels/" + str(data_model_id) + "/dataClasses/" + str(data_class_id)
                    + "/dataClasses",
                    cookies=self.cookie)
            elif id_input and data_class_id is None:
                response = requests.get(
                    self.baseURL + "/api/dataModels/" + data_model_id + "/dataClasses/" + str(id_input),
                    cookies=self.cookie)
            elif id_input and id_input:
                response = requests.get(
                    self.baseURL + "/api/dataModels/" + str(data_model_id) + "/dataClasses/" + str(data_class_id) +
                    "/dataClasses/" + str(id_input),
                    cookies=self.cookie)
        return response

    def get_codesets(self, folder_id=None, codeset_id=None):
        if self.api_key is not None:
            if folder_id is None and codeset_id is None:
                response = requests.get(
                    self.baseURL + "/api/codeSets/",
                    headers={'apiKey': self.api_key})
            elif codeset_id is None:
                response = requests.get(
                    self.baseURL + "/api/folders/" + str(folder_id) + "/codeSets/",
                    headers={'apiKey': self.api_key})
            else:
                response = requests.get(
                    self.baseURL + "/api/codeSets/" + str(codeset_id),
                    headers={'apiKey': self.api_key})
        else:
            if folder_id is None and codeset_id is None:
                response = requests.get(
                    self.baseURL + "/api/codeSets/",
                    cookies=self.cookie)
            elif codeset_id is None:
                response = requests.get(
                    self.baseURL + "/api/folders/" + str(folder_id) + "/codeSets/",
                    cookies=self.cookie)

            else:
                response = requests.get(
                    self.baseURL + "/api/codeSets/" + str(codeset_id),
                    cookies=self.cookie)
        return response

    def get_data_element(self, data_model_id, data_class_id, id_input=None):
        if self.api_key is not None:
            if id_input is None:
                response = requests.get(
                    self.baseURL + "/api/dataModels/" + str(data_model_id) + "/dataClasses/" + str(data_class_id)
                    + "/dataElements",
                    headers={'apiKey': self.api_key})
            else:
                response = requests.get(
                    self.baseURL + "/api/dataModels/" + str(data_model_id) + "/dataClasses/" + str(data_class_id)
                    + "/dataElements/" + str(id_input),
                    headers={'apiKey': self.api_key})
        else:
            if id_input is None:
                response = requests.get(
                    self.baseURL + "/api/dataModels/" + str(data_model_id) + "/dataClasses/" + str(data_class_id)
                    + "/dataElements",
                    cookies=self.cookie)
            else:
                response = requests.get(
                    self.baseURL + "/api/dataModels/" + str(data_model_id) + "/dataClasses/" + str(data_class_id)
                    + "/dataElements/" + str(id_input),
                    cookies=self.cookie)
        return response

    def get_data_model(self, folder_id=None, id_input=None):
        if self.api_key is not None:
            if folder_id is None and id_input is None:
                response = requests.get(
                    self.baseURL + "/api/dataModels",
                    headers={'apiKey': self.api_key})
            elif folder_id is None and id_input is not None:
                response = requests.get(
                    self.baseURL + "/api/dataModels/" + str(id_input),
                    headers={'apiKey': self.api_key})
            else:
                response = requests.get(
                    self.baseURL + "/api/folders/" + str(folder_id) + "/dataModels",
                    headers={'apiKey': self.api_key})
        else:
            if folder_id is None and id_input is None:
                response = requests.get(
                    self.baseURL + "/api/dataModels",
                    cookies=self.cookie)
                return response
            elif folder_id is None and id_input is not None:
                response = requests.get(
                    self.baseURL + "/api/dataModels/" + str(id_input),
                    cookies=self.cookie)
            else:
                response = requests.get(
                    self.baseURL + "/api/folders/" + str(folder_id) + "/dataModels",
                    cookies=self.cookie)
        return response

    def get_versioned_folders(self, folder_id=None, id_input=None):
        if self.api_key is not None:
            if folder_id is None and id_input is None:
                response = requests.get(
                    self.baseURL + "/api/versionedFolders",
                    headers={'apiKey': self.api_key})
            elif folder_id is None and id_input is not None:
                response = requests.get(
                    self.baseURL + "/api/versionedFolders" + str(id_input),
                    headers={'apiKey': self.api_key})
            else:
                response = requests.get(
                    self.baseURL + "/api/folders/" + str(folder_id) + "/versionedFolders",
                    headers={'apiKey': self.api_key})
        else:
            if folder_id is None and id_input is None:
                response = requests.get(
                    self.baseURL + "/api/versionedFolders",
                    cookies=self.cookie)
                return response
            elif folder_id is None and id_input is not None:
                response = requests.get(
                    self.baseURL + "/api/versionedFolders" + str(id_input),
                    cookies=self.cookie)
            else:
                response = requests.get(
                    self.baseURL + "/api/folders/" + str(folder_id) + "/versionedFolders",
                    cookies=self.cookie)
        return response

    def build_versioned_folder(self, json_payload):
        if self.api_key is not None:
            response = requests.post(
                self.baseURL + "/api/versionedFolders",
                headers={'apiKey': self.api_key}, json=json_payload)
        else:
            response = requests.post(
                self.baseURL + "/api/versionedFolders",
                cookies=self.cookie, json=json_payload)
        return response

    def create_data_model(self, folder_id, json_payload):
        """

        Takes a folder ID and JSON payload to create a data model in the specified folder.
        Returns the response

        Example of json payload
        payload={"folder":"ab12f37e-2bf7-314d-b9a0-5133279e66b7","author":"TomHeneghan","description":"InsertDescription",
        "label":"MyLabel","organisation":"ONS","type":"Data Asset","classifiers":[]}

        :param folder_id: String
        :param json_payload: Dictionary or JSON
        :return: Response
        """
        if self.api_key is not None:
            response = requests.post(
                self.baseURL + "/api/folders/"+str(folder_id)+"/dataModels",
                headers={'apiKey': self.api_key}, json=json_payload)
        else:
            response = requests.post(
                self.baseURL + "/api/folders/"+str(folder_id)+"/dataModels",
                cookies=self.cookie, json=json_payload)
        return response


    def build_folder(self, json_payload):
        if self.api_key is not None:
            response = requests.post(
                self.baseURL + "/api/folders",
                headers={'apiKey': self.api_key}, json=json_payload)
        else:
            response = requests.post(
                self.baseURL + "/api/folders",
                cookies=self.cookie, json=json_payload)
        return response


    def create_new_data_class(self, json_payload, data_model_id, data_class_id=None):
        if self.api_key is not None:
            if data_class_id is None:
                response = requests.post(
                    self.baseURL + "/api/dataModels/" + data_model_id +"/dataClasses",
                    headers={'apiKey': self.api_key}, json=json_payload)
            else:
                response = requests.post(
                    self.baseURL + "/api/dataModels/" + data_model_id + "/dataClasses/" + data_class_id +"/dataClasses",
                    headers={'apiKey': self.api_key}, json=json_payload)
        else:
            if data_class_id is None:
                response = requests.post(
                    self.baseURL + "/api/dataModels/" + data_model_id + "/dataClasses",
                    cookies=self.cookie, json=json_payload)
            else:
                response = requests.post(
                    self.baseURL + "/api/dataModels/" + data_model_id + "/dataClasses/" + data_class_id + "/dataClasses",
                   cookies=self.cookie, json=json_payload)
        return response


    def create_data_element(self,json_payload, data_model_id, data_class_id):
        if self.api_key is not None:
            response = requests.post(
                self.baseURL + "/api/dataModels/" + data_model_id +"/dataClasses/" + data_class_id + "/dataElements",
                headers={'apiKey': self.api_key}, json=json_payload)
        else:
            response = requests.post(
                self.baseURL + "/api/dataModels/" + data_model_id +"/dataClasses/" + data_class_id + "/dataElements",
                    cookies=self.cookie, json=json_payload)
        return response

