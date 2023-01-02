import requests
import json

dict1 = {
    "username": "100737",
    "password": "4380",
    "applicationType": 961,
    "iP": "1365"
}
dict1_json = json.dumps(dict1)
r = requests.post(url='http://192.168.20.243:8081/api/Authentication/RequestToken', json=dict1)
token = json.loads(r.text)['token']
expire_date = json.loads(r.text)['expires']

