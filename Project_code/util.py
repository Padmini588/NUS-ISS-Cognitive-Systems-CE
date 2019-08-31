#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Aug 21 11:10:05 2019

@author: shashanknigam
"""

"""
util file
"""

import requests
import datetime

url = "https://tih-api.stb.gov.sg/content/v1/"
API_KEY = "owFO20v6Cw03vt4O4Gk0ENGjSxPAgHsV"

week_day = {
        0:"Monday",
        1:"Tuesday",
        2:"Wednesday",
        3:"Thursday",
        4:"Friday",
        5:"Saturday",
        6:"Sunday"        
        }


def get(url):
    req = requests.get(url)
    print(req.status_code)
    if req.ok:
        return req.json(), req.status_code
    else: 
        return {},req.status_code


def urlUnset():
    global url
    url = "https://tih-api.stb.gov.sg/content/v1/"

    
def urlSet(loc_type,uuid,field):
    urlUnset()
    global url
    url=url+loc_type+"?uuid="+uuid+"&apikey="+API_KEY
    print(url)
    resp,status_code=get(url)
    if status_code==200 and len(resp)!=0:
    
        return resp["data"][0][field]
    else:
        return None

def replace_all(txt,t):
    while txt.find(t)!=-1:
        txt = txt.replace(t,"")
    return txt    


def getBody(loc_type,uuid):
    body = urlSet(loc_type,uuid,"body")
    if body is not None:
        body = replace_all(body,"<div>")
        body = replace_all(body,"</div>")
        body = replace_all(body,"<p>")
        body = replace_all(body,"</p>")
        body = replace_all(body,"<i>")
        body = replace_all(body,"</i>")
        body = replace_all(body,"<br>")
        body = replace_all(body,"<span>")
        body = replace_all(body,"</span>")
        body = replace_all(body,"/")
        body = replace_all(body,"<")
        body = replace_all(body,">")
        body = replace_all(body,"p>")
        body = replace_all(body,"<p")
        body = body.replace("No.","Number")
        body = replace_all(body,"&amp;")
        
        body= body.split(".")        
        b1=[]
        for i in range(len(body)):
            if body[i]!='' and len(body[i])>30:
                b1.append(body[i])
        body = b1
        return body
    else:
        return None

def getAmenities(loc_type,uuid):
    amenities = urlSet(loc_type,uuid,"amenities")    
    if amenities:
        amenities=amenities.split(",")
        return amenities
    else:
        return None

def getImageUrl(loc_type,uuid):
    if uuid=="0020bdb915ebc544abda57063cbeca25582":
        return ["https://www.google.com/url?sa=i&source=images&cd=&ved=2ahUKEwikuoCApJ7kAhWv73MBHXNxASsQjRx6BAgBEAQ&url=https%3A%2F%2Fwww.viator.com%2FSingapore-attractions%2FSkyline-Luge-Sentosa%2Fd18-a27439&psig=AOvVaw3_KRFFnS1QicXfY65D_3DW&ust=1566831401373949"]
    else:
        image=urlSet(loc_type,uuid,"images")
        print(image)
        if image:
            l = len(image)
            image_l=[]
            for i in range(l):
                if image[i]["url"]!="" and image[i]["url"].find("http")!=-1:
                    image_l.append(image[i]["url"])
                else:
                    image_url= "https://tih-api.stb.gov.sg/media/v1/download/uuid/"+image[i]["uuid"]+"?apikey="+API_KEY
                    image_l.append(image_url)
            return image_l
        else:
            return ["https://www.sgphotoforum.com/uploads/default/original/1X/e35f68b40adcb2b667466a95cc48337670be3a7c.jpg"]
 

def getWebsite(loc_type,uuid):
    website=urlSet(loc_type,uuid,"officialWebsite")
    if website:
        if website.find("http")!=-1:
            return website
        else:
            return "http://"+website
    else:
        return None

def getMrt(loc_type,uuid):
    mrt=urlSet(loc_type,uuid,"nearestMrtStation")
    if mrt:
        mrt=mrt.split(",")
        return mrt
    else:
        return None
    
def getDescription(loc_type,uuid):
    description=urlSet(loc_type,uuid,"description")
    if description:
        return description
    else: 
        return None
    
    
def getAwards(loc_type,uuid):
    description=urlSet(loc_type,uuid,"singaporeTourismAwards")
    if description:
        return description
    else:
        return None
 
def getAddress(loc_type,uuid):
    address = urlSet(loc_type,uuid,"address")
    if address:
        s =""
        for key,val in address.items():
           if val!='': 
               s = s+key+" "+val+"\n  "
        return s
    else:
        return None
    
def getPrice(loc_type,uuid):
    price=urlSet(loc_type,uuid,"pricing")
    ticketed = getTicketed(loc_type,uuid)
    print(price)
    if price and ticketed=='Y':
       p_child=price["child"]
       p_adult=price["adult"]
       p_seniorcitizen=price["seniorCitizen"]
       p_others=price["others"]
       if p_child=="" and p_adult=="" and p_seniorcitizen=="" and p_others!="":
           p= p_others.lower()
           print(p)
           if p.find("adult")==-1 and p.find("child")==-1 and p.find("senior")==-1:
               p_child=p_others
           else:
               p_others=p_others.split(',')
               print(p_others)
               if len(p_others)!=1:            
                   for i in range(len(p_others)):
                       if p_others[i].lower().find("adult")!=-1:
                           if p_others[i].find("$")!=-1:
                               p_adult=p_others[i][p_others[i].index("S$")+2:]
                           else:
                               p_adult=p_others[i]
                       elif p_others[i].lower().find("child")!=-1:
                           if p_others[i].find("$")!=-1:
                               p_child=p_others[i][p_others[i].index("S$")+2:]
                           else:
                               p_child=p_others[i]
                       elif p_others[i].lower().find("senior")!=-1:
                           if p_others[i].find("$")!=-1:
                               p_seniorcitizen=p_others[i][p_others[i].index("S$")+2:]
                           else:
                               p_seniorcitizen=p_others[i]        
                       
               elif len(p_others)==1:
                    p_child=p_others[0]
                    p_adult=p_others[0]
               else:
                   if p_child=="":
                        p_child="Free"
                   if p_adult=="":
                       p_adult="Free"
                   if p_seniorcitizen=="":
                       p_seniorcitizen="Free"
       return [p_child,p_adult,p_seniorcitizen,p_others] 
    else:
        return None
    
def getTicketed(loc_type,uuid):
    ticketed=urlSet(loc_type,uuid,"ticketed")    
    if ticketed:
        return ticketed
    else:
        return None

def getSpecialInfo(loc_type,uuid):
    addmissionInfo = urlSet(loc_type,uuid,"addmissionInfo")
    if addmissionInfo:
        return addmissionInfo
    else:
        addmissionInfo = urlSet(loc_type,uuid,"notes")
        if addmissionInfo:
            return addmissionInfo
        else:
            return None
        

def getOpeningTime(loc_type,uuid):
    businessHour = urlSet(loc_type,uuid,"businessHour")
    if businessHour:
        if len(businessHour)==1:
            daily=businessHour[0]["day"]
            if daily=="daily":
                openTime = businessHour[0]["openTime"]
                return openTime
            else: 
                return None
        else:    
            weekday=week_day[datetime.datetime.today().weekday()]
            for i in range(len(businessHour)):
                if weekday==businessHour[i]["day"]:
                    OpenTime = businessHour[i]["openTime"]
                    return OpenTime
            return None
            
def getClosingTime(loc_type,uuid):
    businessHour = urlSet(loc_type,uuid,"businessHour")
    if businessHour:
        if len(businessHour)==1:
            daily=businessHour[0]["day"]
            if daily=="daily":
                closeTime = businessHour[0]["closeTime"]
                return closeTime
        else:    
            weekday=week_day[datetime.datetime.today().weekday()]
            for i in range(len(businessHour)):
                if weekday==businessHour[i]["sequenceNumber"]:
                    closeTime = businessHour[i]["closeTime"]
                    return closeTime
            return None
    else:
        return None
            

def isOpen(loc_type,uuid):
    time = datetime.timedelta(hours=datetime.datetime.today().hour,minutes=datetime.datetime.today().minute,seconds=datetime.datetime.today().second)
    openTime=getOpeningTime(loc_type,uuid)
    if openTime:
        openTime = openTime.split(':')
        o = datetime.timedelta(hours=int(openTime[0]),minutes=int(openTime[1]))
        if o<time:
            closeTime=getClosingTime(loc_type,uuid)
            if closeTime:
                closeTime=closeTime.split(':')
                c=datetime.timedelta(hours=int(closeTime[0]),minutes=int(closeTime[1]))
                if time<c:
                    return True
                else:
                    return False
            else:
                return False
        else:
            return False
    else:
        return False
    
def timeToClose(loc_type,uuid):
    if isOpen(loc_type,uuid):
        time = datetime.timedelta(hours=datetime.datetime.today().hour,minutes=datetime.datetime.today().minute,seconds=datetime.datetime.today().second)
        closeTime=getClosingTime(loc_type,uuid)
        c=datetime.timedelta(hours=int(closeTime[0]),minutes=int(closeTime[1]))
        t = c - time
        hours=int(t.seconds/60/60)
        if hours>0:
            return str(hours)+" hours"
        else:
            minutes=int(t.seconds/60)
            return str(minutes)+" minutes"
    else:
        return timeToOpen(loc_type,uuid) + " to Open"

def timeToOpen(loc_type,uuid):
    if not isOpen(loc_type,uuid):
        time = datetime.timedelta(hours=datetime.datetime.today().hour,minutes=datetime.datetime.today().minute,seconds=datetime.datetime.today().second)
        OpenTime=getOpeningTime(loc_type,uuid)
        c=datetime.timedelta(hours=int(OpenTime[0]),minutes=int(OpenTime[1]))
        t = time - c
        hours=int(t.seconds/60/60)
        if hours>0:
            return str(hours)+" hours"
        else:
            minutes=int(t.seconds/60)
            return str(minutes)+" minutes"
    else:
        return timeToClose(loc_type,uuid) + "to  close"      
        
    
def nextOpen(loc_type,uuid):
    if not isOpen(loc_type,uuid):
        daynum = datetime.datetime.today().weekday()
        businessHour = urlSet(loc_type,uuid,"businessHour")
        if businessHour:
            days=[]
            
            if businessHour[0]["day"] =="daily":
                openTime =businessHour[0]["openTime"]
                return "It will next  open at "+openTime
            else:
                for i in range(len(businessHour)):
                    days.append(businessHour[i]["day"])
                for i in range(1,7):
                    if week_day[(daynum+i)%7] in days:
                        for j in businessHour:
                            if j["day"]==week_day[(daynum+i)%7]:
                                openTime = j["openTime"]
                                return "It will next  open on coming"+ week_day[(daynum+i)%7]+" at "+openTime
            return None
        else: 
            return None
    else:
        return "Its Open today"
                
            
        

def getReviewList(loc_type,uuid):
  reviewInfo = urlSet(loc_type,uuid,"reviews")
  if reviewInfo:
      return reviewInfo
  else:
      return None
                
