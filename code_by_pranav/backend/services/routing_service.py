import requests
import os

ORS_API_KEY = os.getenv("ORS_API_KEY")

def get_route(start, end):
    url = "https://api.openrouteservice.org/v2/directions/driving-car"
    headers = {
        "Authorization": ORS_API_KEY,
        "Content-Type": "application/json"
    }
    body = {
        "coordinates": [start[::-1], end[::-1]]
    }
    response = requests.post(url, headers=headers, json=body)
    return response.json()
