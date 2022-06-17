"""
This doc lists commonly required JSON formats and contains functions that will generate JSONs.
By default, the functions return python dictionaries as opposed to JSON unless return_json is set to true,
This is because python dictionaries are handled in the pymauro methods as the json argument.
"""

import json


def versioned_folder_json(label, return_json=False):
    dict_form= {"label": label}
    json_form=json.dumps(dict_form)
    if return_json:
        return json_form
    else:
        return dict_form



def standard_folder_json(label, return_json=False):
    dict_form= {"label": label}
    json_form=json.dumps(dict_form)
    if return_json:
        return json_form
    else:
        return dict_form


def data_asset_json(folder_id, label, type='Data Asset', classifiers=None,
                    description=None, author=None, organisation=None, return_json=False):
    if type not in ['Data Asset', 'Data Standard']:
        return ValueError("type mut be one of Data Asset or Data Standard")
    if classifiers is None:
        classifiers = []
    if description is None:
        description = ""
    if author is None:
        author = ""
    if organisation is None:
        organisation = ""
    dict_form = {"folder": folder_id, "label": label, "description": description,
            "author": author, "organisation": organisation, "type": type, "classifiers": classifiers}
    json_form = json.dumps(dict_form)
    if return_json:
        return json_form
    else:
        return dict_form

def data_model_json(folder_id, label, type='Data Standard', classifiers=None,
                    description=None, author=None, organisation=None, return_json=False):
    if type not in ['Data Asset', 'Data Standard']:
        return ValueError("type mut be one of Data Asset or Data Standard")
    if classifiers is None:
        classifiers = []
    if description is None:
        description = ""
    if author is None:
        author = ""
    if organisation is None:
        organisation = ""
    dict_form = {"folder": folder_id, "label": label, "description": description,
            "author": author, "organisation": organisation, "type": type, "classifiers": classifiers}
    json_form = json.dumps(dict_form)
    if return_json:
        return json_form
    else:
        return dict_form

def data_class_json(label, domainType="DataClass", description=None, classifiers=None, metadata=None,
                    minMultiplicity=None, maxMultiplicity=None, return_json=False):
    if classifiers is None:
        classifiers = []
    if metadata is None:
        metadata = []
    dict_form= {"domainType": domainType, "label": label, "classifiers": classifiers, "description":description,
                "metadata": metadata, "minMultiplicity": minMultiplicity, "maxMultiplicity": maxMultiplicity}
    json_form = json.dumps(dict_form)
    if return_json:
        return json_form
    else:
        return dict_form

def data_element_json(label, datatype=None, domainType="DataElement", description=None, classifiers=None,
                      metadata=None,
                      minMultiplicity=None, maxMultiplicity=None, return_json=False):
    if datatype is None:
        datatype = {"id": ""}
    if classifiers is None:
        classifiers = []
    if metadata is None:
        metadata = []
    if description is None:
        description = ""
    dict_form = {"domainType": domainType, "label": label, "description": description, "dataType": datatype,
                "classifiers": classifiers, "metadata": metadata, "minMultiplicity": minMultiplicity,
                "maxMultiplicity": maxMultiplicity}
    json_form = json.dumps(dict_form)
    if return_json:
        return json_form
    else:
        return dict_form

def data_type_json(label, domainType="PrimitiveType", description=None, organisation=None,
                   classifiers=None, metadata=None, referenceClass=None, referenceDataType=None,
                   modelResourceDomainType=None, enumerationValues=None, modelResourceId=None, return_json=False):
    if referenceClass is None:
        referenceClass = {"id": ""}
    if referenceDataType is None:
        referenceDataType = {"id": ""}
    if enumerationValues is None:
        enumerationValues = []
    if organisation is None:
        organisation = ""
    dict_form = {"label": label, "description": description, "organisation": organisation, "domainType": domainType,
                "referenceDataType": referenceDataType, "referenceClass": referenceClass,
                "modelResourceDomainType": modelResourceDomainType, "modelResourceId": modelResourceId,
                "classifiers": classifiers, "enumerationValues": enumerationValues, "metadata": metadata}
    json_form = json.dumps(dict_form)
    if return_json:
        return json_form
    else:
        return dict_form

def add_profile_to_data_model_json(metadata_namespace, data_model_id, data_model_label, applicable_domains='',
                                   return_json=False):
    dict_form = {'sections':
        [
            {'name': 'Profile Specification',
             'description': 'The details necessary for this Data Model to be used as the specification for a dynamic profile.',
             'fields': [
                 {'fieldName': 'Metadata namespace', 'metadataPropertyName': 'metadataNamespace',
                  'description': 'The namespace under which properties of this profile will be stored',
                  'maxMultiplicity': 1, 'minMultiplicity': 1, 'allowedValues': None, 'regularExpression': None,
                  'dataType': 'string', 'derived': False, 'derivedFrom': None, 'uneditable': False,
                  'defaultValue': None, 'editableAfterFinalisation': True, 'currentValue': metadata_namespace},
                 {'fieldName': 'Applicable for domains', 'metadataPropertyName': 'domainsApplicable',
                  'description': "Determines which types of catalogue item can be profiled using this profile.  For example, 'DataModel'.  Separate multiple domains with a semi-colon (';').  Leave blank to allow this profile to be applicable to any catalogue item.",
                  'maxMultiplicity': 1, 'minMultiplicity': 0, 'allowedValues': None, 'regularExpression': None,
                  'dataType': 'string', 'derived': False, 'derivedFrom': None, 'uneditable': False,
                  'defaultValue': None, 'editableAfterFinalisation': True, 'currentValue': applicable_domains},
                 {'fieldName': 'Can be edited after finalisation', 'metadataPropertyName': 'editableAfterFinalisation',
                  'description': 'Defines if the profile can be edited after the model has been finalised. This defaults to false.',
                  'maxMultiplicity': 1, 'minMultiplicity': 0, 'allowedValues': None, 'regularExpression': None,
                  'dataType': 'boolean', 'derived': False, 'derivedFrom': None, 'uneditable': False,
                  'defaultValue': None, 'editableAfterFinalisation': True, 'currentValue': ''}]}],
        'id': data_model_id, 'label': data_model_label, 'domainType': 'DataModel',
        'namespace': 'uk.ac.ox.softeng.maurodatamapper.profile', 'name': 'ProfileSpecificationProfileService'}
    json_form = json.dumps(dict_form)
    if return_json:
        return json_form
    else:
        return dict_form


def add_profile_to_data_element_json(data_element_id, data_element_label, return_json=False):
    dict_form = {'sections':
          [{'name': 'Profile Specification', 'description': 'The details necessary for this Data Element to define a field for a dynamic profile.', 'fields':
        [{'fieldName': 'Metadata Property Name', 'metadataPropertyName': 'metadataPropertyName', 'description': 'The key under which this property of this profile will be stored', 'maxMultiplicity': 1, 'minMultiplicity': 1, 'allowedValues': None, 'regularExpression': None, 'dataType': 'string', 'derived': False, 'derivedFrom': None, 'uneditable': False, 'defaultValue': None, 'editableAfterFinalisation': True, 'currentValue': ''},
        {'fieldName': 'Default Value', 'metadataPropertyName': 'defaultValue', 'description': 'The default value that will be offered for this property', 'maxMultiplicity': 1, 'minMultiplicity': 0, 'allowedValues': None, 'regularExpression': None, 'dataType': 'string', 'derived': False, 'derivedFrom': None, 'uneditable': False, 'defaultValue': None, 'editableAfterFinalisation': True, 'currentValue': ''},
        {'fieldName': 'Regular expression', 'metadataPropertyName': 'regularExpression', 'description': 'A regular expression that may be used to validate string fields', 'maxMultiplicity': 1, 'minMultiplicity': 0, 'allowedValues': None, 'regularExpression': None, 'dataType': 'string', 'derived': False, 'derivedFrom': None, 'uneditable': False, 'defaultValue': None, 'editableAfterFinalisation': True, 'currentValue': ''},
        {'fieldName': 'May be edited after finalisation', 'metadataPropertyName': 'editableAfterFinalisation', 'description': 'If the owning model is editable after finalisation, determines whether this field may be edited after the owning model has been finalised', 'maxMultiplicity': 1, 'minMultiplicity': 1, 'allowedValues': None, 'regularExpression': None, 'dataType': 'boolean', 'derived': False, 'derivedFrom': None, 'uneditable': False, 'defaultValue': None, 'editableAfterFinalisation': True, 'currentValue': 'true'}]}],
           'id': data_element_id, 'label': data_element_label, 'domainType': 'DataElement', 'namespace': 'uk.ac.ox.softeng.maurodatamapper.profile', 'name': 'ProfileSpecificationFieldProfileService'}
    json_form = json.dumps(dict_form)
    if return_json:
        return json_form
    else:
        return dict_form