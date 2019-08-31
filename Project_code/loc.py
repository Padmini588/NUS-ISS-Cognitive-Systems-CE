import requests
import math
import pandas as pd
import os.path as path
API_KEY="owFO20v6Cw03vt4O4Gk0ENGjSxPAgHsV"
def find_distance(lat1,lng1,lat2,lng2):
  R=6731000
  phi1 = lat1
  phi2 = lat2
  delta1 = phi2-phi1
  lam = lng2-lng1
  a = math.sin(delta1/2)*math.sin(delta1/2) + math.cos(phi1)*math.cos(phi2)*math.sin(lam/2)*math.sin(lam/2)
  c = 2*math.atan2(math.sqrt(a),math.sqrt(1-a))
  d = R*c
  return d
def loc(lat1,lng1,lat2,lng2,dist):
  d=find_distance(lat1,lng1,lat2,lng2)
  return d<=dist
def find_nearby(loc_dict,uuid,dist):
  lat1=loc_dict[loc_dict["uuid"]==uuid].lat
  lng1=loc_dict[loc_dict["uuid"]==uuid].lng
  l=[]
  for i in range(len(loc_dict)):
      if(loc(lat1,lng1,loc_dict["lat"][i],loc_dict["lng"][i],dist)):
          l.append(i)
  return(l)
def get(url):
  resp = requests.get(url)
  print(resp.status_code)
  if resp.ok:
      return resp.json(),resp.status_code
  else:
      return "{}",resp.status_code
def create_dic():
  loc_dict={}
  if not path.exists("loc.csv"):
      uuid=[]
      name=[]
      lat=[]
      lng=[]
      t=[]
      tags=[]
      cusine=[]
      categoryDescription=[]
      rating=[]
      rownum=[]
      datasets=["attractions","bars_clubs","food_beverages","shops"]
      nexttoken=""
      for data in datasets:
          print(data)
          url=f"https://tih-api.stb.gov.sg/content/v1/search/all?dataset={data}&apikey={API_KEY}"
          d1,status_code=get(url)
          while status_code == 200:
              d=d1["data"]["results"]
              nexttoken=d1["nextToken"]
              for i in range(len(d)):
                  if d[i]["name"] not in name:
                      uuid.append(d[i]["uuid"])
                      name.append(d[i]["name"])
                      lat.append(math.radians(d[i]["location"]["latitude"]))
                      lng.append(math.radians(d[i]["location"]["longitude"]))
                      t.append(d[i]["type"])
                      tags.append(d[i]["tags"])
                      rating.append(d[i]["rating"])
                      if data in ["food_beverages"]:
                          cusine.append(d[i]["cuisine"])
                      else:
                          cusine.append("")
                      categoryDescription.append(d[i]["categoryDescription"])
              url=f"https://tih-api.stb.gov.sg/content/v1/search/all?dataset={data}&nextToken={nexttoken}&apikey={API_KEY}"
              d1,status_code = get(url)
      for i in range(0,len(uuid)):
        rownum.append(i)
      loc_dict={"uuid":uuid,"name":name,"lat":lat,"lng":lng,"type":t,"tags":tags,"cusine":cusine,"categoryDescription":categoryDescription,"rating":rating}
      loc_dict=pd.DataFrame(loc_dict)
      loc_dict.sort_values('rating', inplace=True, ascending=False)
      loc_dict['rownum'] = rownum
      loc_dict.to_csv('loc.csv')
  else:
      loc_dict=pd.read_csv('loc.csv')
  return pd.DataFrame(loc_dict)
