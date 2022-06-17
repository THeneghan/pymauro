import xml.etree.ElementTree as ET




def simple_erwin_xml_parse(erwin_xml):
    profile_constructor_json ={}
    profile_names=[]
    parsed_xml=ET.parse(erwin_xml)
    high_level_objects = list(parsed_xml.iter('Entity'))
    for entities in high_level_objects:
        profile_names.append(entities.attrib['Name'])
        my_key=entities.attrib['Name']
        my_val=[]
        attribute_groups=entities.find('Attribute_Groups')
        attributes = attribute_groups.findall('Attribute')
        attribute_props=[attribute.find('AttributeProps') for attribute in attributes]
        for items in attribute_props:
            for properties in items:
                if properties.tag == 'Name':
                    #my_val={properties.text:[]}
                    inter=properties.text
                    my_val.append(inter)
                profile_constructor_json[my_key]=my_val
    return profile_constructor_json

def complex_erwin(erwin_xml):
    profile_constructor_json = {}
    profile_names = []
    parsed_xml = ET.parse(erwin_xml)
    high_level_objects = list(parsed_xml.iter('Entity'))
    for entities in high_level_objects:
        profile_names.append(entities.attrib['Name'])
        my_key = entities.attrib['Name']
        my_val = []
        attribute_groups = entities.find('Attribute_Groups')
        attributes = attribute_groups.findall('Attribute')
        attribute_props = [attribute.find('AttributeProps') for attribute in attributes]
        for items in attribute_props:
            my_dict={}
            for properties in items:
                my_dict[properties.tag]=properties.text
            my_val.append(my_dict)
            profile_constructor_json[my_key] = my_val
    return profile_constructor_json


print(complex_erwin('erwinexprt3.xml'))
