import requests
import json

pld = '{"username":"thomas.heneghan@ons.gov.uk","password":"Dredds1996!"}'
json_payload= json.loads(pld)
print(json_payload)
print(type(json_payload))


url="https://modelcatalogue.cs.ox.ac.uk/ons/api/authentication/login"

response=requests.post(url,json=json_payload)
print(response.json())