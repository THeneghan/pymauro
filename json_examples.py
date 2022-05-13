"""
This doc lists commonly required example JSONs
"""
import json

example_versioned_folder_json={"label":"My first versioned folder"}
example_standard_folder_json={"label": "My first standard folder"}

def versioned_folder_json(label):
    return {"label":label}

def standard_folder_json(label):
    return {"label":label}

def standard_data_model(folder_id, label, type='Data Asset', classifiers=None,
                        description=None, author=None, organisation=None):
    if type not in ['Data Asset','Data Standard']:
        return ValueError("type mut be one of Data Asset or Data Standard")
    if classifiers is None:
        classifiers = []
    if description is None:
        description=""
    if author is None:
        author =""
    if organisation is None:
        organisation = ""
    return {"folder":folder_id,"label":label,"description":description,
            "author":author, "organisation":organisation,"type":type,"classifiers":classifiers}


def standard_data_class(label,domainType="DataClass", classifiers=None, metadata=None,
                        minMultiplicity=None, maxMultiplicity=None):
    if classifiers is None:
        classifiers = []
    if metadata is None:
        metadata = []
    pre_json = {"domainType":domainType,"label":label,"classifiers":classifiers,
                "metadata":metadata, "minMultiplicity":minMultiplicity, "maxMultiplicity":maxMultiplicity}
    return pre_json


