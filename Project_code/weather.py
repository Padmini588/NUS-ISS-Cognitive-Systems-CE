import requests
from tempfile import TemporaryFile
import math
import loc
import xlrd
import xlwt

def get(url):
    resp = requests.get(url)
    if resp.ok:
        return resp.json()
    
def getWeatherdata():
 book = xlwt.Workbook()   
 url = "https://tih-api.stb.gov.sg/weather/v1/2hr-forecast?apikey=Jnk5CX0HRfQPbClS5oMa9X0LDt4XvF1r"
 print(url)
 data = get(url)
 areaList=[]    
 wetaherList=[] 
 Longitude=[]
 Latitude=[]
 for x in range(0,len(data['data'])):
           areaList.insert(x,data['data'][x]['area'])
           wetaherList.insert(x,data['data'][x]['forecast'])
       
 
 sheet1 = book.add_sheet('sheet1')

 for i,e in enumerate(areaList):
    sheet1.write(i,0,e)
    
 for i,e in enumerate(wetaherList):
    sheet1.write(i,1,e)
 

 for x in range(0,len(data['data'])):
  url = f"https://api.opencagedata.com/geocode/v1/geojson?q={data['data'][x]['area']}&key=45c4fc17862b4504b8e130b2503313ff&pretty=1"
  locData = get(url)
  Longitude.insert(x,locData['features'][0]['geometry']['coordinates'][0])
  Latitude.insert(x,locData['features'][0]['geometry']['coordinates'][1])

 for i,e in enumerate(Longitude):
    sheet1.write(i,2,e)
 for i,e in enumerate(Latitude):
    sheet1.write(i,3,e)
 name = "weather.xls"
 book.save(name)
 book.save(TemporaryFile())
 
 
def getWeather(lat,long):
 xl_workbook = xlrd.open_workbook('weather.xls')
 xl_sheet = xl_workbook.sheet_by_name('sheet1')
 Latitude=[]
 wetaherList=[]
 Longitude=[]
 for row_idx in range(0, xl_sheet.nrows):
        Latitude.append(xl_sheet.cell_value(row_idx, 3))
        
 for row_idx in range(0, xl_sheet.nrows):
        Longitude.append(xl_sheet.cell_value(row_idx, 2))
        
 for row_idx in range(0, xl_sheet.nrows):
        wetaherList.append(xl_sheet.cell_value(row_idx, 1))
        
        
 distance=[]
 for x in range(0,len(Latitude)):
     distance.insert(x,loc.find_distance(lat,long,math.radians(Latitude[x]),math.radians(Longitude[x])))
 
 minDistPos = distance.index(min(distance)) 
 return wetaherList[minDistPos]
 