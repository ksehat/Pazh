import requests
import json
import pandas as pd

data = {
  "origin": "THR",
  "destination": "MHD",
  "days": 4
}

r = requests.post(url='http://192.168.40.155:2000', data=json.dumps(data))
df = pd.DataFrame(columns=r.json()['columns'], data=r.json()['data'])
df.to_sql()