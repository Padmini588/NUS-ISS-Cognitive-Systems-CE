import requests
import math

def get(url):
    resp = requests.get(url)
    if resp.ok:
        return resp.json()
    
    
def getlatlong(area):
  url = f"https://api.opencagedata.com/geocode/v1/geojson?q={area}&key=45c4fc17862b4504b8e130b2503313ff&pretty=1"
  locData = get(url)
  Latitude =locData['features'][0]['geometry']['coordinates'][1]
  Longitude = locData['features'][0]['geometry']['coordinates'][0]
  return math.radians(Latitude),math.radians(Longitude)

