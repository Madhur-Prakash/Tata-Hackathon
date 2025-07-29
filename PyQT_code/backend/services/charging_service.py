import requests

def get_nearest_station(lat, lng):
    url = f"https://api.openchargemap.io/v3/poi/?output=json&latitude={lat}&longitude={lng}&distance=5&key=DEMO"
    res = requests.get(url)
    if res.status_code == 200 and res.json():
        top = res.json()[0]
        return {
            "name": top["AddressInfo"]["Title"],
            "lat": top["AddressInfo"]["Latitude"],
            "lon": top["AddressInfo"]["Longitude"]
        }
    return {}
