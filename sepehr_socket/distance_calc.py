import requests
import random


endpoint = "https://api.openrouteservice.org/v2/directions/driving-car"
api_key = "5b3ce3597851110001cf6248cbd35d490fd743bfae7ce0bcf4c68655"

origin = [random.uniform(26, 27), random.uniform(35, 36)] #long, lat
destination = [random.uniform(26, 27), random.uniform(35, 36)]

payload = { "coordinates": [origin, destination], "format": "geojson", "instructions": False, "elevation": False, "extra_info": ["steepness"], }

response = requests.post(endpoint, json=payload, headers={"Authorization": api_key})
distance = response.json()["features"][0]["properties"]["segments"][0]["distance"]
print(distance)