"""pymauro is an opensource library that wraps the REST API endpoints of a Mauro Data Mapper instance into a Python
library to allow easy, automated development.

Currently, documentation is lacking but the functionality can be approximately described by viewing the methods
as described in the documentation for the analogous Client library at
https://maurodatamapper.github.io/resources/client/java/#binding-vs-non-binding-clients

Details on the endpoints themselves can be found at:
https://maurodatamapper.github.io/rest-api/introduction/#testing

Classes:
    BaseClient

Functions:
    test_my_url() - Not proven to work

"""
import requests
import json_examples


def test_my_url(url, **kwargs):
    """
Takes the url (string) and appends /api/test.
This new path is then sent a get request. The response is
returned. This function has not been proven to work - suspected endpoint mistake

    :param url: The base url of the Mauro instance
    :return: :class:`Response` object
    """
    print("This function has not been proven to work - suspected endpoint mistake")
    response = requests.get(url + "/api/test", **kwargs)
    return response


class BaseClient:
    """
    A class to connect to a Mauro Data Mapper instance.

    It is recommended that you provide both a username/password and API key as some methods only operate off the
    provision of one and not the other.

    The user must provide at least a username and password or an API key. A type error will return if the arguments
    provided do not abide by this rule. When possible the called method will use the API key over the session id created
    by login via username/password to prevent session time-outs.


    Attributes
    ----------
    baseurl : str
        The base URL of the Mauro instance
    username : str
        Login username
    password : str
        Login password
    api_key: str
        The API key to authenticate
    cookie: requests.cookies.RequestsCookieJar
        Auto generated cookie to pass as argument for requests


    Methods
    -------
    test_my_connection
    check_for_valid_session
    logout
    admin_check
    list_api_keys
    create_new_api_key
    delete_api_key
    enable_api_key
    disable_api_key
    refresh_api_key
    list_folders
    get_metadata
    permissions
    post_metadata
    get_classifiers
    get_data_classes
    get_codesets
    get_data_element
    get_data_model
    get_versioned_folder
    create_versioned_folder
    create_data_model
    create_folder
    create_new_data_class
    update_data_class
    create_data_element
    method_constructor

    Each method possesses its own docstring.


    """

    def __init__(self, baseurl, username=None, password=None, api_key=None):
        self._baseURL = baseurl  # Non-public to prevent accidental editing
        self._username = username  # Non-public to prevent accidental editing
        self.__password = password  # Name mangled to prevent accidental disclosure
        self.api_key = api_key
        if (self._username is None or self.__password is None) and self.api_key is None \
                or self._username is not None and self.__password is None \
                or self._username is None and self.__password is not None:
            raise TypeError("You must provide at a minimum: the username and password as a pairing or an API Key.")
        if self._username is not None and 'id' in self.test_my_connection().json().keys():
            self.cookie = self.test_my_connection().cookies
        else:
            self.cookie = None

    @property
    def username(self):
        return self._username

    @property
    def baseURL(self):
        return self._baseURL

    def __repr__(self):
        return "Mauro Client Object"

    def test_my_connection(self, **kwargs):
        """
        Executes a post request with username and password as json payload to the baseurl appended with
        /api/authentication/login. The response is returned.

        :return: :class:`Response' object
        """
        if self.username is None:
            raise TypeError("You must provide a username and password to access this method")
        json_payload = dict(username=self.username, password=self.__password)
        response = requests.post(self.baseURL + "/api/authentication/login", json=json_payload, **kwargs)
        return response

    def check_for_valid_session(self,**kwargs):
        """
        Executes a get request to the url + /api/session/isAuthenticated
        with the session ID in the cookies header.
        The response is returned.

        :return: :class:`Response' object
        """
        if self.username is None:
            raise TypeError("You must provide a username and password to access this method")
        response = requests.get(self.baseURL + "/api/session/isAuthenticated", cookies=self.cookie, **kwargs)
        return response

    def logout(self, **kwargs):
        """
        A logout get request is sent to baseurl appended with /api/authentication/logout with the session ID in the
        cookies header. The response is returned.

        :return: :class:`Response' object
        """
        if self.username is None:
            raise TypeError("You must provide a username and password to access this method")
        response = requests.get(self.baseURL + "/api/authentication/logout", cookies=self.cookie, **kwargs)
        return response

    def admin_check(self, **kwargs):
        """
        Get request to determine whether user is an admin.

        :return: :class:`Response' object
        """
        if self.api_key is not None:
            response = requests.get(self.baseURL + "/api/session/isApplicationAdministration",
                                    headers={'apiKey': self.api_key}, **kwargs)
        else:
            response = requests.get(self.baseURL + "/api/session/isApplicationAdministration",
                                    cookies=self.cookie, **kwargs)
        return response

    def list_api_keys(self, catalogue_user_id=None, **kwargs):
        """
        Lists api keys.

        If catalogue_user_id is provided, request will return response for request using the provided catalogue
        as opposed to current user's default value.

        :param catalogue_user_id: - (optional) A catalogue user id
        :return: :class:`Response' object
        """
        if self.username is None and catalogue_user_id is None:
            raise TypeError("A username/password or an id "
                            "method argument is required for this method to work")
        elif self.api_key is None and catalogue_user_id is None:
            default_id = self.test_my_connection().json()['id']
            response = requests.get(self.baseURL + "/api/catalogueUsers/" + default_id + "/apiKeys",
                                    cookies=self.cookie, **kwargs)
        elif self.api_key is None and catalogue_user_id is not None:
            response = requests.get(self.baseURL + "/api/catalogueUsers/" + catalogue_user_id + "/apiKeys",
                                    cookies=self.cookie, **kwargs)
        elif self.api_key is not None and catalogue_user_id is None:
            default_id = self.test_my_connection().json()['id']
            response = requests.get(self.baseURL + "/api/catalogueUsers/" + default_id + "/apiKeys",
                                    headers={'apiKey': self.api_key}, **kwargs)
        elif self.api_key is not None and catalogue_user_id is not None:
            response = requests.get(self.baseURL + "/api/catalogueUsers/" + catalogue_user_id + "/apiKeys",
                                    headers={'apiKey': self.api_key}, **kwargs)
        return response

    def create_new_api_key(self, key_name='My First Key', expiry=365, refreshable=True, catalogue_user_id=None, **kwargs):
        """
        Creates a new API key depending on arguments provided,

        If catalogue_user_id is provided, request will return response for request using the provided catalogue
        as opposed to current user's default value.

        :param key_name: The name of the created key. Default value is 'My First Key'
        :param expiry: int - Number of days until key expiry. Default value is 365.
        :param refreshable: bool - Make key refreshable. Default value is True.
        :param catalogue_user_id: - (optional) A catalogue user id
        :return: :class:`Response' object
        """
        if self.username is None and catalogue_user_id is None:
            raise TypeError("A username/password or an id "
                            "method argument is required for this method to work")
        elif self.api_key is not None:
            json_payload = dict(name=key_name, expiresInDays=expiry, refreshable=refreshable)
            if catalogue_user_id is None:
                default_id = self.test_my_connection().json()['id']
                response = requests.post(self.baseURL + "/api/catalogueUsers/" + default_id + "/apiKeys",
                                         headers={'apiKey': self.api_key}, json=json_payload, **kwargs)
            else:
                response = requests.post(self.baseURL + "/api/catalogueUsers/" + catalogue_user_id + "/apiKeys",
                                         headers={'apiKey': self.api_key}, json=json_payload, **kwargs)
        else:
            if catalogue_user_id is None:
                json_payload = dict(name=key_name, expiresInDays=expiry, refreshable=refreshable)
                default_id = self.test_my_connection().json()['id']
                response = requests.post(self.baseURL + "/api/catalogueUsers/" + default_id + "/apiKeys",
                                         cookies=self.cookie, json=json_payload, **kwargs)
            else:
                json_payload = dict(name=key_name, expiresInDays=expiry, refreshable=refreshable)
                response = requests.post(self.baseURL + "/api/catalogueUsers/" + catalogue_user_id + "/apiKeys",
                                         cookies=self.cookie, json=json_payload, **kwargs)
        return response

    def delete_api_key(self, key_to_delete, catalogue_user_id=None, **kwargs):
        """
        Deletes API key.

        If catalogue_user_id is provided, request will return response for request using the provided catalogue
        as opposed to current user's default value.

        :param key_to_delete: API key id to delete
        :param catalogue_user_id: - (optional) A catalogue user id
        :return: :class:`Response' object
        """
        if self.username is None and catalogue_user_id is None:
            raise TypeError("A username/password or an id "
                            "method argument is required for this method to work")
        elif self.api_key is not None:
            if catalogue_user_id is None:
                default_id = self.test_my_connection().json()['id']
                response = requests.delete(
                    self.baseURL + "/api/catalogueUsers/" + str(default_id) + "/apiKeys/" + str(key_to_delete),
                    headers={'apiKey': self.api_key}, **kwargs)
            else:
                response = requests.delete(
                    self.baseURL + "/api/catalogueUsers/" + catalogue_user_id + "/apiKeys/" + str(key_to_delete),
                    headers={'apiKey': self.api_key}, **kwargs)
            return response
        else:
            if catalogue_user_id is None:
                default_id = self.test_my_connection().json()['id']
                print(default_id)
                response = requests.delete(
                    self.baseURL + "/api/catalogueUsers/" + str(default_id) + "/apiKeys/" + str(key_to_delete),
                    cookies=self.cookie, **kwargs)
            else:
                response = requests.delete(
                    self.baseURL + "/api/catalogueUsers/" + catalogue_user_id + "/apiKeys/" + str(key_to_delete),
                    cookies=self.cookie, **kwargs)
            return response

    def disable_api_key(self, key_to_disable, catalogue_user_id=None, **kwargs):
        """
        Disables API key

        If catalogue_user_id is provided, request will return response for request using the provided catalogue
        as opposed to current user's default value.

        :param key_to_disable: API key to disable
        :param catalogue_user_id: - (optional) A catalogue user id
        :return: :class:`Response' object
        """
        if self.username is None and catalogue_user_id is None:
            raise TypeError("A username/password or an id "
                            "method argument is required for this method to work")
        elif self.api_key is not None:
            if catalogue_user_id is None:
                default_id = self.test_my_connection().json()['id']
                response = requests.put(self.baseURL + "/api/catalogueUsers/" + str(default_id) + "/apiKeys/"
                                        + str(key_to_disable) + "/disable", headers={'apiKey': self.api_key}, **kwargs)
            else:
                response = requests.put(self.baseURL + "/api/catalogueUsers/" + catalogue_user_id + "/apiKeys/"
                                        + str(key_to_disable) + "/disable", headers={'apiKey': self.api_key}, **kwargs)
            return response
        else:
            if catalogue_user_id is None:
                default_id = self.test_my_connection().json()['id']
                response = requests.put(self.baseURL + "/api/catalogueUsers/" + str(default_id) + "/apiKeys/"
                                        + str(key_to_disable) + "/disable", cookies=self.cookie, **kwargs)
            else:
                response = requests.put(self.baseURL + "/api/catalogueUsers/" + catalogue_user_id + "/apiKeys/"
                                        + str(key_to_disable) + "/disable", cookies=self.cookie, **kwargs)
            return response

    def enable_api_key(self, key_to_enable, catalogue_user_id=None, **kwargs):
        """
        Disables API key

        If catalogue_user_id is provided, request will return response for request using the provided catalogue
        as opposed to current user's default value.

        :param key_to_enable: API key to enable
        :param catalogue_user_id: - (optional) A catalogue user id
        :return: :class:`Response' object
        """
        if self.username is None and catalogue_user_id is None:
            raise TypeError("A username/password or an id argument is required for this method to work")
        elif self.api_key is not None:
            if catalogue_user_id is None:
                default_id = self.test_my_connection().json()['id']
                response = requests.put(self.baseURL + "/api/catalogueUsers/" + default_id + "/apiKeys/"
                                        + str(key_to_enable) + "/enable", headers={'apiKey': self.api_key}, **kwargs)
            else:
                response = requests.put(self.baseURL + "/api/catalogueUsers/" + catalogue_user_id + "/apiKeys/" +
                                        str(key_to_enable) + "/enable", headers={'apiKey': self.api_key}, **kwargs)
        else:
            if catalogue_user_id is None:
                default_id = self.test_my_connection().json()['id']
                response = requests.put(self.baseURL + "/api/catalogueUsers/" + str(default_id) + "/apiKeys/"
                                        + str(key_to_enable) + "/enable", cookies=self.cookie, **kwargs)
            else:
                response = requests.put(self.baseURL + "/api/catalogueUsers/" + catalogue_user_id + "/apiKeys/" +
                                        str(key_to_enable) + "/enable", cookies=self.cookie, **kwargs)
        return response

    def refresh_api_key(self, key_to_refresh, days_until_expiry=365, catalogue_user_id=None):
        """
        Refreshes API key

        If catalogue_user_id is provided, request will return response for request using the provided catalogue
        as opposed to current user's default value.

        :param key_to_refresh: API key to refresh
        :param days_until_expiry: int - Number of days until key expiry. Default value is 365
        :param catalogue_user_id: - (optional) A catalogue user id
        :return: :class:`Response' object
        """
        if self.username is None and catalogue_user_id is None:
            raise TypeError("A username/password or an id "
                            "method argument is required for this method to work")
        elif self.api_key is not None:
            if catalogue_user_id is None:
                default_id = self.test_my_connection().json()['id']
                response = requests.put(self.baseURL + "/api/catalogueUsers/" + str(default_id) + "/apiKeys/"
                                        + str(key_to_refresh) + "/refresh/" + str(days_until_expiry),
                                        headers={'apiKey': self.api_key})
            else:
                response = requests.put(self.baseURL + "/api/catalogueUsers/" + catalogue_user_id + "/apiKeys/" +
                                        str(key_to_refresh) + "/refresh/" + str(days_until_expiry),
                                        headers={'apiKey': self.api_key})
            return response
        else:
            if catalogue_user_id is None:
                default_id = self.test_my_connection().json()['id']
                response = requests.put(self.baseURL + "/api/catalogueUsers/" + str(default_id) + "/apiKeys/"
                                        + str(key_to_refresh) + "/refresh/" + str(days_until_expiry),
                                        cookies=self.cookie)
            else:
                response = requests.put(self.baseURL + "/api/catalogueUsers/" + catalogue_user_id + "/apiKeys/" +
                                        str(key_to_refresh) + "/refresh/" + str(days_until_expiry),
                                        cookies=self.cookie)
            return response

    def list_folders(self, folder_id=None, specific_id=None, offset=0, max_limit=10, show_all=False):
        """
        Lists the folders present in a Mauro instance.

        :param offset: int - pagination offset value. Default value = 0
        :param max_limit: int - maximum number of folders returned. Default value = 10
        :param show_all: bool - show all folders (overrides max and offset limit). Default value = False
        :return: :class:`Response' object
        """
        if folder_id is None and specific_id is None:
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
        elif specific_id is None:
            if self.api_key is not None:
                if not show_all:
                    response = requests.get(
                        self.baseURL + "/api/folders/" + folder_id +"/folders?offset=" + str(offset) + "&max=" + str(max_limit),
                        headers={'apiKey': self.api_key})
                else:
                    response = requests.get(self.baseURL + "/api/folders/" +folder_id+"/folders?all=true", headers={'apiKey': self.api_key})

            else:
                if not show_all:
                    response = requests.get(
                        self.baseURL + "/api/folders" +folder_id+"/folders/?offset=" + str(offset) + "&max=" + str(max_limit),
                        cookies=self.cookie)

        elif folder_id is None:
            if self.api_key is not None:
                    response = requests.get(
                        self.baseURL + "/api/folders/" + specific_id,
                        headers={'apiKey': self.api_key})

            else:
                    response = requests.get(
                        self.baseURL + "/api/folders/" +folder_id,
                        cookies=self.cookie)
        else:
            if self.api_key is not None:
                    response = requests.get(
                        self.baseURL + "/api/folders/" + folder_id + "/folders/"+specific_id,
                        headers={'apiKey': self.api_key})

            else:
                    response = requests.get(
                        self.baseURL + "/api/folders/" + folder_id + "/folders/"+specific_id,
                        cookies=self.cookie)

        return response

    def get_metadata(self, catalogue_item_domain_type, catalogue_item_id, metadata_id=None):
        """
        Get the metadata information on a catalogue item or metadata item within a catalogue id.

        :param catalogue_item_domain_type: Must be one of "folders", "dataModels", "dataClasses", "dataTypes",
         "terminologies", "terms" or "referenceDataModels".
        :param catalogue_item_id: The id of the catalogue item.
        :param metadata_id: - (optional) A catalogue user id.
        :return: :class:`Response' object.
        """
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

    def permissions(self, catalogue_item_domain_type, catalogue_item_id):
        """
        Get the permissions of a catalogue item id

        :param catalogue_item_domain_type: Must be one of "folders", "dataModels", "dataClasses",
        "dataTypes", "terminologies", "terms" or "referenceDataModels"
        :param catalogue_item_id: The catalogue item id
        :return: :class:`Response' object
        """
        val_domain_types = ["folders", "dataModels", "dataClasses", "dataTypes", "terminologies", "terms",
                            "referenceDataModels"]
        if catalogue_item_domain_type not in val_domain_types:
            raise ValueError("catalogueItemDomainType must be in " + str(val_domain_types))
        if self.api_key is not None:
            response = requests.get(self.baseURL + "/api/" + str(catalogue_item_domain_type) + "/" +
                                    str(catalogue_item_id) + "/permissions",
                                    headers={'apiKey': self.api_key})
            return response
        else:
            response = requests.get(
                self.baseURL + "/api/" + str(catalogue_item_domain_type) + "/" + str(catalogue_item_id) +
                "/permissions", cookies=self.cookie)
            return response

    def post_metadata(self, catalogue_item_domain_type, catalogue_item_id, namespace_inp, key_val, value_inp):
        """
        Post metadata

        :param catalogue_item_domain_type: Must be one of "folders", "dataModels", "dataClasses",
        "dataTypes", "terminologies", "terms" or "referenceDataModels".
        :param catalogue_item_id: The catalogue item id.
        :param namespace_inp: The namespace
        :param key_val: The key
        :param value_inp: The value
        :return: :class:`Response' object
        """
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

    def get_classifiers(self, classifier_id=None, id_input=None):
        """
        Get classifiers - paginated list or specific id

        :param classifier_id: Parent classifier id
        :param id_input: Child classifier id
        :return: :class:`Response' object
        """
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
        """
        Get data classes - paginated list or specific id

        :param data_model_id: The data model id
        :param data_class_id: The data class id
        :param id_input: Specific data class id
        :return: :class:`Response' object
        """
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
        """
        Get codesets - paginated list or specific id

        :param folder_id: The folder id
        :param codeset_id: Specific codeset id
        :return: :class:`Response' object
        """
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
        """
        Get data element - paginated list or specific id

        :param data_model_id: The data model id
        :param data_class_id: The data class id
        :param id_input: Specific data element id
        :return: :class:`Response' object
        """
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
        """
        Get data model - paginated list or specific id

        :param folder_id: The folder id
        :param id_input: Specific data model id
        :return: :class:`Response' object
        """
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
        """
        List versioned folders - paginated list or specific id

        :param folder_id: The folder id
        :param id_input: Specific versioned folder id
        :return: :class:`Response' object
        """
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

    def create_versioned_folder(self, json_payload):
        """
        Builds a versioned folder

        :param json_payload: json data to send in the body of the :class: 'Request'
        :return: :class:`Response' object
        """
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
        Creates a data model in the specified folder

        :param folder_id: Folder id to create data model in
        :param json_payload: json data to send in the body of the :class: 'Request'
        :return: :class:`Response' object
        """
        if self.api_key is not None:
            response = requests.post(
                self.baseURL + "/api/folders/" + str(folder_id) + "/dataModels",
                headers={'apiKey': self.api_key}, json=json_payload)
        else:
            response = requests.post(
                self.baseURL + "/api/folders/" + str(folder_id) + "/dataModels",
                cookies=self.cookie, json=json_payload)
        return response

    def create_folder(self, json_payload, folder_id=None):
        """
        Build a new folder.

        :param json_payload: json data to send in the body of the :class: 'Request'
        :param folder_id: - (optional) The folder id to build the new folder within
        :return: :class:`Response' object
        """
        if folder_id is None:
            if self.api_key is not None:
                response = requests.post(
                    self.baseURL + "/api/folders",
                    headers={'apiKey': self.api_key}, json=json_payload)
            else:
                response = requests.post(
                    self.baseURL + "/api/folders",
                    cookies=self.cookie, json=json_payload)
        else:
            if self.api_key is not None:
                response = requests.post(
                    self.baseURL + "/api/folders/" + folder_id + "/folders",
                    headers={'apiKey': self.api_key}, json=json_payload)
            else:
                response = requests.post(
                    self.baseURL + "/api/folders/" + folder_id + "/folders",
                    cookies=self.cookie, json=json_payload)

        return response

    def create_new_data_class(self, json_payload, data_model_id, data_class_id=None):
        """
        Create a new data class

        :param json_payload: json data to send in the body of the :class: 'Request'
        :param data_model_id: The data model id to which the new class will belong
        :param data_class_id: - (optional) The data class id to which the new class will belong
        :return: :class:`Response' object
        """
        if self.api_key is not None:
            if data_class_id is None:
                response = requests.post(
                    self.baseURL + "/api/dataModels/" + data_model_id + "/dataClasses",
                    headers={'apiKey': self.api_key}, json=json_payload)
            else:
                response = requests.post(
                    self.baseURL + "/api/dataModels/" + data_model_id + "/dataClasses/"
                    + data_class_id + "/dataClasses",
                    headers={'apiKey': self.api_key}, json=json_payload)
        else:
            if data_class_id is None:
                response = requests.post(
                    self.baseURL + "/api/dataModels/" + data_model_id + "/dataClasses",
                    cookies=self.cookie, json=json_payload)
            else:
                response = requests.post(
                    self.baseURL + "/api/dataModels/" + data_model_id +
                    "/dataClasses/" + data_class_id + "/dataClasses",
                    cookies=self.cookie, json=json_payload)
        return response

    def update_data_class(self, json_payload, data_model_id, data_class_id=None, **kwargs):
        """
        Updates a data class

        :param json_payload: json data to send in the body of the :class: 'Request'
        :param data_model_id: The data model id to which the class belongs
        :param data_class_id: The data class to update
        :return: :class:`Response' object
        """
        if self.api_key is not None:
            if data_class_id is None:
                response = requests.put(
                    self.baseURL + "/api/dataModels/" + data_model_id,
                    headers={'apiKey': self.api_key}, json=json_payload, **kwargs)
            else:
                response = requests.put(
                    self.baseURL + "/api/dataModels/" + data_model_id + "/dataClasses/" + data_class_id,
                    headers={'apiKey': self.api_key}, json=json_payload, **kwargs)
        else:
            if data_class_id is None:
                response = requests.put(
                    self.baseURL + "/api/dataModels/" + data_model_id,
                    cookies=self.cookie, json=json_payload, **kwargs)
            else:
                response = requests.put(
                    self.baseURL + "/api/dataModels/" + data_model_id + "/dataClasses/" + data_class_id,
                    cookies=self.cookie, json=json_payload, **kwargs)
        return response

    def create_data_element(self, json_payload, data_model_id, data_class_id, **kwargs):
        """
        Creates a data element

        :param json_payload: json data to send in the body of the :class: 'Request'
        :param data_model_id: The data model id to which the element should belong
        :param data_class_id: The data class id to which the element should belong
        :return: :class:`Response' object
        """
        if self.api_key is not None:
            response = requests.post(
                self.baseURL + "/api/dataModels/" + data_model_id + "/dataClasses/" + data_class_id + "/dataElements",
                headers={'apiKey': self.api_key}, json=json_payload, **kwargs)
        else:
            response = requests.post(
                self.baseURL + "/api/dataModels/" + data_model_id + "/dataClasses/" + data_class_id + "/dataElements",
                cookies=self.cookie, json=json_payload, **kwargs)
        return response

    def method_constructor(self, command, json_payload=None, *args, **kwargs):
        """
        A generalised way of creating any endpoint. Any additional arguments provided via args will be appended
        to baseurl allowing custom endpoints to be rapidly built.

        :param command: String value that must be one of 'put', 'post', 'get' or 'delete'
        :param json_payload: - (optional) json data to send in the body of the :class: 'Request'
        :param args: - (optional) String to compose endpoints
        :return: :class:`Response' object
        """
        if command not in ['put', 'post', 'get', "delete"]:
            raise ValueError("Must be put, post, delete or get")
        append_string = ""
        for vals in args:
            append_string = append_string + vals
        if self.api_key is not None:
            if command == "put":
                response = requests.put(self.baseURL + append_string,
                                        headers={'apiKey': self.api_key}, json=json_payload, **kwargs)
            elif command == "post":
                response = requests.post(self.baseURL + append_string,
                                         headers={'apiKey': self.api_key}, json=json_payload, **kwargs)
            elif command == "get":
                response = requests.get(self.baseURL + append_string,
                                        headers={'apiKey': self.api_key}, json=json_payload, **kwargs)
            elif command == "delete":
                response = requests.delete(self.baseURL + append_string,
                                           headers={'apiKey': self.api_key}, json=json_payload, **kwargs)
        else:
            if command == "put":
                response = requests.put(self.baseURL + append_string,
                                        cookies=self.cookie, json=json_payload, **kwargs)
            elif command == "post":
                response = requests.post(self.baseURL + append_string,
                                         cookies=self.cookie, json=json_payload, **kwargs)
            elif command == "get":
                response = requests.get(self.baseURL + append_string,
                                        cookies=self.cookie, json=json_payload, **kwargs)
            elif command == "delete":
                response = requests.delete(self.baseURL + append_string,
                                           cookies=self.cookie, json=json_payload, **kwargs)
        return response

    def delete_folder(self, folder_id, parent_folder_id=None, permanent=False, **kwargs):
        """

        Parameters
        ----------
        folder_id
        parent_folder_id
        permanent

        Returns
        -------

        """
        admin_rights = self.admin_check().json()
        if admin_rights['applicationAdministrationSession'] != True:
            raise ValueError("Admin rights not detected")

        if permanent == False:
            bool_val = "false"
        elif permanent == True:
            bool_val = "true"
        if self.api_key is not None:
            if parent_folder_id is None:
                response = requests.delete(self.baseURL + "/api/folders/" +
                                           folder_id + "?permanent=" + bool_val,
                                           headers={'apiKey': self.api_key},**kwargs)
            else:
                response = requests.delete(self.baseURL + "/api/folders/" + parent_folder_id +
                                           "/folders/" + folder_id + "?permanent=" + bool_val,
                                           headers={'apiKey': self.api_key},**kwargs)
        else:
            if parent_folder_id is None:
                response = requests.delete(self.baseURL + "/api/folders/" +
                                           folder_id + "?permanent=" + bool_val,
                                           cookies=self.cookie,**kwargs)
            else:
                response = requests.delete(self.baseURL + "/api/folders/" + parent_folder_id +
                                           "/folders/" + folder_id + "?permanent=" + bool_val,
                                           cookies=self.cookie,**kwargs)
        return response

    def delete_data_model(self, data_model_id, permanent=False, **kwargs):
        """

        Parameters
        ----------


        Returns
        -------

        """
        admin_rights = self.admin_check().json()
        if admin_rights['applicationAdministrationSession'] != True:
            raise ValueError("Admin rights not detected")

        if permanent == False:
            bool_val = "false"
        elif permanent == True:
            bool_val = "true"
        if self.api_key is not None:
                response = requests.delete(self.baseURL + "/api/dataModels/" + data_model_id +
                                           "?permanent=" + bool_val,
                                           headers={'apiKey': self.api_key},**kwargs)
        else:
            response = requests.delete(self.baseURL + "/api/dataModels/" + data_model_id +
                                       "?permanent=" + bool_val,
                                        cookies=self.cookie,**kwargs)
        return response

    def purge_instance(self):
        """

        Returns
        -------

        """
        admin_rights = self.admin_check().json()
        if admin_rights['applicationAdministrationSession'] != True:
            raise ValueError("Admin rights not detected")
        print("WARNING -THIS IS IRREVERSIBLE: Do you want to delete the entire contents of the Mauro instance (y/n)?")
        del_input = input()
        if del_input not in ["y", "Y", "Yes", "yes", "n", "N", "no", "No"]:
            return ValueError("Must be y/yes/Y/Yes or n/N/No/no")
        if del_input in ["y", "Y", "Yes", "yes"]:
            key_list = self.list_folders().json().keys()
            if 'items' in key_list:
                parent_array = self.list_folders().json()['items']
                for els in parent_array:
                    folder_ids = (els['id'])
                    self.delete_folder(folder_ids, permanent=True)
                return "All folders deleted"
            else:
                return ("Purge not possible")

        else:
            return ("Purge cancelled")

    def purge_folder(self, folder_id):
        """

        Returns
        -------

        """
        admin_rights = self.admin_check().json()
        if admin_rights['applicationAdministrationSession'] != True:
            raise ValueError("Admin rights not detected")
        print("WARNING: Do you want to delete the entire contents of this folder (y/n)?")
        del_input = input()
        if del_input not in ["y", "Y", "Yes", "yes", "n", "N", "no", "No"]:
            return ValueError("Must be y/yes/Y/Yes or n/N/No/no")
        if del_input in ["y", "Y", "Yes", "yes"]:
            key_list1 = self.get_data_model(folder_id).json().keys()
            key_list2 = self.list_folders(folder_id).json().keys()
            if 'items' in key_list1:
                parent_array_data_models = self.get_data_model(folder_id).json()['items']
                for els in parent_array_data_models:
                     data_model_ids = (els['id'])
                     self.delete_data_model(data_model_ids, permanent=True)
            if 'items' in key_list2:
                parent_array_folders= self.list_folders(folder_id).json()['items']
                for els in parent_array_folders:
                    folder_ids = (els['id'])
                    self.delete_folder(folder_ids, permanent=True)
        else:
             return ("Purge cancelled")

    def create_data_type(self, data_model_id, json_payload, **kwargs):
        if self.api_key is not None:
            response = requests.post(
                self.baseURL + "/api/dataModels/" + data_model_id + "/dataTypes",
                headers={'apiKey': self.api_key}, json=json_payload, **kwargs)
        else:
            response = requests.post(
                self.baseURL + "/api/dataModels/" + data_model_id + "/dataTypes",
                cookies=self.cookie, json=json_payload, **kwargs)
        return response


    def get_data_types(self, data_model_id=None, specific_id=None, **kwargs):
        if data_model_id is None:
            if self.api_key is not None:
                response = requests.get(
                    self.baseURL + "/api/dataModels/defaultDataTypeProviders",
                    headers={'apiKey': self.api_key}, **kwargs)
            else:
                response = requests.get(
                    self.baseURL + "/api/dataModels/defaultDataTypeProviders",
                    cookies=self.cookie, **kwargs)
        elif specific_id is None:
            if self.api_key is not None:
                response = requests.get(
                    self.baseURL + "/api/dataModels/" + data_model_id +"/dataTypes",
                    headers={'apiKey': self.api_key}, **kwargs)
            else:
                response = requests.get(
                    self.baseURL + "/api/dataModels/" + data_model_id +"/dataTypes",
                    cookies=self.cookie, **kwargs)
        else:
            if self.api_key is not None:
                response = requests.get(
                    self.baseURL + "/api/dataModels/" + data_model_id + "/dataTypes/" + specific_id ,
                    headers={'apiKey': self.api_key}, **kwargs)
            else:
                response = requests.get(
                    self.baseURL + "/api/dataModels/" + data_model_id + "/dataTypes/" + specific_id,
                    cookies=self.cookie, **kwargs)
        return response



    def create_data_profile(self, folder_id, json_payload, **kwargs):
        """
        Creates a data profile in the specified folder

        :param folder_id: Folder id to create data model in
        :param json_payload: json data to send in the body of the :class: 'Request'
        :return: :class:`Response' object
        """
        if self.api_key is not None:
            response = requests.post(
                self.baseURL + "/api/folders/" + str(folder_id) +
                "/dataModels?defaultDataTypeProvider=ProfileSpecificationDataTypeProvider",
                headers={'apiKey': self.api_key}, json=json_payload, **kwargs)
        else:
            response = requests.post(
                self.baseURL + "/api/folders/" + str(folder_id) +
                "/dataModels?defaultDataTypeProvider=ProfileSpecificationDataTypeProvider",
                cookies=self.cookie, json=json_payload, **kwargs)
        return response


    def add_data_profile_to_data_model(self, data_model_id, json_payload, **kwargs):
        if self.api_key is not None:
            response = requests.post(
                self.baseURL + "/api/dataModels/" + str(data_model_id) +
                "/profile/uk.ac.ox.softeng.maurodatamapper.profile/ProfileSpecificationProfileService",
                headers={'apiKey': self.api_key}, json=json_payload, **kwargs)
        else:
            response = requests.post(
                self.baseURL + "/api/dataModels/" + str(data_model_id) +
                "/profile/uk.ac.ox.softeng.maurodatamapper.profile/ProfileSpecificationProfileService",
                cookies=self.cookie, json=json_payload, **kwargs)
        return response

    def add_data_profile_to_data_element(self, data_element_id, json_payload, **kwargs):
        if self.api_key is not None:
            print(self.baseURL + "/api/dataElements/" + str(data_element_id) +
                "/profile/uk.ac.ox.softeng.maurodatamapper.profile/ProfileSpecificationFieldProfileService")
            print("http://localhost:8082/api/dataElements/22ff7b97-b452-4cef-b9bf-4833f5888dad/profile/uk.ac.ox.softeng.maurodatamapper.profile/ProfileSpecificationFieldProfileService")
            response = requests.post(
                self.baseURL + "/api/dataElements/" + str(data_element_id) +
                "/profile/uk.ac.ox.softeng.maurodatamapper.profile/ProfileSpecificationFieldProfileService",
                headers={'apiKey': self.api_key}, json=json_payload, **kwargs)
        else:
            response = requests.post(
                self.baseURL + "/api/dataElements/" + str(data_element_id) +
                "/profile/uk.ac.ox.softeng.maurodatamapper.profile/ProfileSpecificationFieldProfileService",
                cookies=self.cookie, json=json_payload, **kwargs)
        return response

    def populate_folder_with_data_asset_models(self,data_model_list, folder_id, type='Data Asset',classifiers=None,
                    description=None, author=None, organisation=None, return_json=False):
        log_list=[]
        for model in data_model_list:
            json_package= json_examples.data_asset_json(folder_id,model,type=type,classifiers=classifiers,
                    description=description, author=author, organisation=organisation, return_json=return_json)
            hit=self.create_data_model(folder_id,json_package)
            log_list.append(hit)
        return log_list

    def populate_item_with_data_classes(self,data_class_list,data_model_id, data_class_id=None):
        for cls in data_class_list:
            json_payload=json_examples.data_class_json(cls)
            self.create_new_data_class(json_payload,data_model_id,data_class_id)


    def populate_data_class_with_elements(self, elements_list,data_model_id, data_class_id, datatype=None, domainType="DataElement", description=None, classifiers=None,
                      metadata=None,
                      minMultiplicity=None, maxMultiplicity=None, return_json=False):

        for els in elements_list:
            print(self.create_data_element(json_examples.data_element_json(els,datatype=datatype,domainType="DataElement",description=description, classifiers=classifiers,
                      metadata=metadata,
                      minMultiplicity=minMultiplicity, maxMultiplicity=maxMultiplicity, return_json=return_json),data_model_id,data_class_id).json())


    def add_profile_to_all_class_data_elements(self, data_model_id, data_class_id):
        items=self.get_data_element(data_model_id,data_class_id).json()['items']
        for item in items:
            element_id=item['id']
            element_label=item['label']
            print(element_id, element_label)
            json_payload = json_examples.add_profile_to_data_element_json(element_id,element_label)
            self.add_data_profile_to_data_element(element_id,json_payload)

    def create_profiles_from_erwin_json(self, erwin_json, folder_id):
        generated_model_ids=[]
        generated_class_ids=[]
        generated_element_ids=[]
        model_class_elements={}
        profile_list=[]
        for profile_names in erwin_json:
             profile_list.append(profile_names)
             new_data_model=self.create_data_profile(folder_id,json_examples.data_model_json(folder_id,profile_names,
                                                                                             description="Profile for " + profile_names)).json()['id']
             generated_model_ids.append(new_data_model)
             new_data_class=self.create_new_data_class(data_model_id=new_data_model,
                                        json_payload=json_examples.data_class_json(str(profile_names+" properties"),
                                                                                   description=profile_names +" technical properties")).json()['id']
             generated_class_ids.append(new_data_class)
             model_class_elements_key=(new_data_model,new_data_class)
             model_class_elements[model_class_elements_key]=erwin_json[profile_names]
        for keys in model_class_elements:
            data_types=self.get_data_types(data_model_id=keys[0]).json()['items']
            for types in data_types:
                if types['label']=='string':
                    for vals in model_class_elements[keys]:
                        generated_element_ids.append(self.create_data_element(json_examples.data_element_json(vals['Name'],datatype={"id":types['id']}, description=vals['Definition']),keys[0],keys[1]).json())
        counter=0
        for ids in generated_model_ids:
            self.add_data_profile_to_data_model(ids,json_examples.add_profile_to_data_model_json("",ids,profile_list[counter]))
            counter=counter+1
        for ids in generated_element_ids:
            print(ids)
            self.add_data_profile_to_data_element(ids['id'],json_examples.add_profile_to_data_element_json(ids['id'],ids['label']))

    def list_all_profile_providers(self, **kwargs):
        if self.api_key is not None:
            response = requests.get(self.baseURL + "/api/profiles/providers",
                                    headers={'apiKey': self.api_key}, **kwargs)
        else:
            response = requests.get(self.baseURL + "/api/profiles/providers",
                                    cookies=self.cookie, **kwargs)
        return response

    def list_all_dynamic_profile_providers(self, **kwargs):
        if self.api_key is not None:
            response = requests.get(self.baseURL + "/api/profiles/providers/dynamic",
                                    headers={'apiKey': self.api_key}, **kwargs)
        else:
            response = requests.get(self.baseURL + "/api/profiles/providers/dynamic",
                                    cookies=self.cookie, **kwargs)
        return response

    def list_used_profiles_for_profiled_object(self,**kwargs):
        if self.api_key is not None:
            response = requests.get(self.baseURL + "/api/profiles/providers/dynamic",
                                    headers={'apiKey': self.api_key}, **kwargs)
        else:
            response = requests.get(self.baseURL + "/api/profiles/providers/dynamic",
                                    cookies=self.cookie, **kwargs)
        return response

    def list_profiles_used_by_data_class(self, data_class_id, **kwargs):
        if self.api_key is not None:
            response = requests.get(self.baseURL + "/api/dataClasses/" + data_class_id+"/profiles/used",
                                    headers={'apiKey': self.api_key}, **kwargs)
        else:
            response = requests.get(self.baseURL + "/api/dataClasses/" + data_class_id+"/profiles/used",
                                    cookies=self.cookie, **kwargs)
        return response



    # Currently not working
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
