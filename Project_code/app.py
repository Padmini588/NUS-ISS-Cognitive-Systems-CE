#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Aug 15 18:09:29 2019

@author: shashanknigam
"""

from flask import request,Response,Flask,json
import loc
import response
import util
import findlocations
import math
import random
import getloc
#import pandas as pd

#Initializing the keys
loc_dict=loc.create_dic()
user_name=''
name=''
user_lat=''
user_lgn=''
categoryDescription=''
number_adults=''
number_children=''
occassion=''
tags = ''
uuid =''
cusine = ''
attraction_type=["Others","Leisure & Recreation","Adventure","Nature & Wildlife","History & Culture","Arts"]
bars_type=["Bars","Clubs","Others"]
restuarant_type=["Restaurants","Hawker Centres","Others","Cafe"]
malls_type = ["Boutiques","Malls","Bazaars & Flea Markets","Department Store"]
cat_description={'Attractions':'attractions','Bars & Clubs':'bars-clubs','Food & Beverages':'food-beverages','Malls & Shops':'shops'}
#,"Find Other Place"


priceC =0
priceA = 0
priceS = 0
priceO = 0
loc_prop = ["Get More Info","How to get there","Reviews","Is Open","Get Fare","Open Time","Close Time","Nearest MRT"]

def reset_all():
    global user_name
    global name
    global user_lat
    global user_lgn
    global user_name
    global name
    global user_lat
    global user_lgn
    global categoryDescription
    global number_adults
    global number_children
    global occassion
    global cusine
    global attraction_types
    global bars_type
    global malls_type
    global priceC
    global priceA
    global priceS
    global priceO
    global loc_prop
    global tags
    global uuid
    global attraction_type
    global restuarant_type
    global cat_description
    findlocations.utilreset()
    user_name=''
    name=''
    user_lat=''
    user_lgn=''
    categoryDescription=''
    number_adults=''
    number_children=''
    occassion=''
    tags = ''
    uuid =''
    cusine = ''
    attraction_type=["Others","Leisure & Recreation","Adventure","Nature & Wildlife","History & Culture","Arts"]
    bars_type=["Bars","Clubs","Others"]
    restuarant_type=["Restaurants","Hawker Centres","Others","Cafe"]
    malls_type = ["Boutiques","Malls","Bazaars & Flea Markets","Department Store"]
    cat_description={'Attractions':'attractions','Bars & Clubs':'bars-clubs','Food & Beverages':'food-beverages','Malls & Shops':'shops'}
    priceC =0
    priceA = 0
    priceS = 0
    priceO = 0
    loc_prop = ["Get More Info","How to get there","Reviews","Is Open","Get Fare","Open Time","Close Time","Nearest MRT"]
    findlocations.utilreset()
    
def set_type():
    global attraction_type
    global bars_type
    global restuarant_type
    global malls_type
    attraction_type=["Others","Leisure & Recreation","Adventure","Nature & Wildlife","History & Culture","Arts"]
    bars_type=["Bars","Clubs","Others"]
    restuarant_type=["Restaurants","Hawker Centres","Others","Cafe"]
    malls_type = ["Boutiques","Malls","Bazaars & Flea Markets","Department Store"]


def remove_type(types=None):
    if types:
        global attraction_type
        global bars_type
        global restuarant_type
        global malls_type
        if categoryDescription=="Attractions" and len(attraction_type)>1:
            attraction_type.remove(types)
        elif categoryDescription=="Bars & Clubs" and len(bars_type)>1:
            bars_type.remove(types)
        elif categoryDescription=="Food & Beverages" and len(restuarant_type)>1:
            restuarant_type.remove(types)
        elif categoryDescription == "Malls & Shops" and len(malls_type)>1:
            malls_type.remove(types)

def setloc_prop():
    global loc_prop
    global categoryDescription
    if categoryDescription=="Attractions":
        loc_prop = ["Get More Info","Reviews","Is Open","Get Fare","Open Time","Close Time","Nearest MRT","How to get there","Show Similar places","Show different place"]
    elif categoryDescription=="Bars & Clubs":
        loc_prop = ["Get More Info","Reviews","Is Open","Open Time","Close Time","Nearest MRT","How to get there","Show Similar places","Show different place"]
    elif categoryDescription=="Food & Beverages":
        loc_prop = ["Get More Info","Reviews","cusine","Is Open","Open Time","Close Time","Nearest MRT","How to get there","Show Similar places","Show different place"] 
    elif categoryDescription == "Malls & Shops":
        loc_prop = ["Get More Info","Reviews","Is Open","Open Time","Close Time","Nearest MRT","How to get there","Show Similar places","Show different place"]
        


def DefaultWelcome():
    reset_all()
    resp = response.permissions(["NAME"],"Hi There, this is your Yellow Pages a congnitive chat bot. What can I call you?")
    return resp


def mainMenu():
    l=["Find Places near me","Shopping","Find Food","Attractions","Bars & Clubs"]
    sug = response.suggesstions(l)
    resp=response.responseSuggestions(f"How can I help you today?",sug)
    return resp



def actions_intent_PERMISSION(req):
    global user_name
    global user_lat
    global user_lgn
    global categoryDescription
    permissionGranted=req["originalDetectIntentRequest"]["payload"]["inputs"][0]["arguments"][0]["textValue"]
    permissionAsked = req["originalDetectIntentRequest"]["payload"]["user"]["permissions"]
    resp = {}
    if "NAME" in permissionAsked and "DEVICE_PRECISE_LOCATION" not in permissionAsked:
        resp=mainMenu()
        sug = response.suggesstions(["met before","know more"])
        if permissionGranted=="true":
            user_name=req["originalDetectIntentRequest"]["payload"]['user']['profile']['givenName']
            resp=response.responseSuggestions(f"Hey {user_name},Have we met before or would you like to know more about me?",sug)
        else:
            resp=response.responseSuggestions(f"Have we met before or would you like to know more about me?",sug)
    elif "DEVICE_PRECISE_LOCATION" in permissionAsked: 
        if permissionGranted=="true" and user_lat=='' and user_lgn=='' and categoryDescription=='':
            sug = response.suggesstions(["Attraction","Shopping","Find Food"])
            user_lat = math.radians(req["originalDetectIntentRequest"]["payload"]["device"]['location']['coordinates']['latitude'])
            user_lgn = math.radians(req["originalDetectIntentRequest"]["payload"]["device"]['location']['coordinates']['longitude'])
            resp = response.responseSuggestions("What would you like to do today?",sug)
        elif permissionGranted=="true" and user_lat=='' and user_lgn=='' and categoryDescription!='':
            user_lat = math.radians(req["originalDetectIntentRequest"]["payload"]["device"]['location']['coordinates']['latitude'])
            user_lgn = math.radians(req["originalDetectIntentRequest"]["payload"]["device"]['location']['coordinates']['longitude'])
            if categoryDescription=="Attractions":
                sug = response.suggesstions(["Adventure","Arts","History & Culture","Leisure & Recreation","Nature & WildLife","Others"])
            elif categoryDescription=="Bars & Clubs":
                sug = response.suggesstions(bars_type)
            elif categoryDescription=="Food & Beverages":    
                sug = response.suggesstions(restuarant_type)
            elif categoryDescription=="Malls & Shops":
                sug = response.suggesstions(malls_type)
            setloc_prop()
            if categoryDescription=="Food & Beverages":
                sug = response.suggesstions(["Yes","No"])
                resp = response.responseSuggestions(f"Are you looking for some specific cusine?",sug)
            else:    
                resp=response.responseSuggestions(f"Which kind of activity are you currently interested in?",sug)
                return resp
        else: 
            resp=mainMenu()
    else:
        resp=mainMenu()    
    return resp




def metBefore():
    sug = response.suggesstions(["Find Places near me","Shopping","Find Food","Attractions","Bars & Clubs"])
    if user_name!='':
        resp=response.responseSuggestions(f"{user_name},How can I help you today?",sug)
    else:
        resp=response.responseSuggestions(f"How can I help you today?",sug)
    return resp    





def knowMore():
    sug = response.suggesstions(["Find Places near me","Shopping","Find Food","Attractions"])
    if user_name!='':
        resp=response.responseSuggestions(f"{user_name},I am Yellow Pages a congnitive chat bot. Your complete on the go companion around Singapore. I can tell interesting facts about places and help you get around places in your locality. How can I help you today?",sug)
    else:
        resp=response.responseSuggestions(f"I am Yellow Pages a congnitive chat bot. Your complete on the go companion around Singapore. I can tell interesting facts about places and help you get around places in your locality. How can I help you today?",sug)
    return resp
   
def nearMe():
    resp = response.permissions(["DEVICE_PRECISE_LOCATION"],"Can we know your location?")
    return resp

def attraction(resp):
    print(resp)
    global categoryDescription
    global tags
    global loc_prop
    print(loc_prop)
    categoryDescription=resp['queryResult']['parameters']['categoryDescription']
    print(categoryDescription)
    categoryDescription=categoryDescription.title()
    if categoryDescription=="Attractions":
        sug = response.suggesstions(["Adventure","Arts","History & Culture","Leisure & Recreation","Nature & WildLife","Others"])
    elif categoryDescription=="Bars & Clubs":
        sug = response.suggesstions(bars_type)
    elif categoryDescription=="Food & Beverages":    
        sug = response.suggesstions(restuarant_type)
    elif categoryDescription=="Malls & Shops":
        sug = response.suggesstions(malls_type)
    setloc_prop()
    print(loc_prop)
    if categoryDescription=="Food & Beverages":
        sug = response.suggesstions(["Yes","No"])
        resp = response.responseSuggestions(f"Are you looking for some specific cusine?",sug)
    else: 
        resp=response.responseSuggestions(f"Which kind of activity are you currently interested in?",sug)
    return resp




def attractionTypes(resp):
    global occassion
    global tags
    global name
    oc=resp['queryResult']['parameters']['attraction_type']
    oc=oc.title()
    print(oc)
    print(oc in attraction_type)
    if oc in attraction_type or oc in bars_type or oc in bars_type or oc in restuarant_type or oc in malls_type:
        occassion = oc
        d=findlocations.getEntity(categoryDescription=categoryDescription,types=occassion,lat=user_lat,lng=user_lgn)
    else:
        tags = oc
        d=findlocations.getEntity(categoryDescription=categoryDescription,tag=tags,lat=user_lat,lng=user_lgn)
    if len(d)==1:
        if oc in attraction_type or oc in bars_type or oc in bars_type or oc in restuarant_type or oc in malls_type:
            occassion = oc
            d=findlocations.getEntity(categoryDescription=categoryDescription,types=occassion,lat=user_lat,lng=user_lgn)
        else:
            tags = oc
            d=findlocations.getEntity(categoryDescription=categoryDescription,tag=tags,lat=user_lat,lng=user_lgn)
    
    names = []
    image=''
    carousel=[]
    Distance = []
    for i in d:
        names.append(str(loc_dict[loc_dict["uuid"]==i]["name"].iloc[0]))
        desc = f"Here are few places of your interest"
    if user_lat and user_lgn:
        if name!='':
            desc = f"Here are few places of your interest near {name}"
        for i in d:
            lat = float(loc_dict[loc_dict["uuid"]==i]["lat"].iloc[0])
            lgn = float(loc_dict[loc_dict["uuid"]==i]["lng"].iloc[0])
            dis= loc.find_distance(float(user_lat),float(user_lgn),float(lat),float(lgn))
            if dis>=1000:
                dis = round(dis/1000,2)
                dis = "Distance:"+str(dis) + " kms"
            else:
                dis = round(dis,2)
                dis = "Distance:"+str(dis) +" mts"
            Distance.append(dis)
    else:
         desc= "Here are some top rated place of your interest"
         for i in d:
            print(i)
            rating = loc_dict[loc_dict["uuid"]==i]["rating"].iloc[0]
            rating = "Rated:"+str(rating)+" stars"
            Distance.append(rating)
    for i in range(len(d)):
        img=util.getImageUrl(cat_description[categoryDescription],d[i])
        if img is None:
            carousel.append(response.createCarouselWImage(names[i],names[i]))
        else:    
            image=(response.image(img[0],names[i]))
            carousel.append(response.createCarouselDesc(names[i],image,Distance[i],names[i]))
    sug = response.suggesstions(["Show Similar Places","Show different Places"])        
    req = response.respCarouselS(carousel,desc,sug)
    print(req)
    return req

def locationName(req):
    global loc_prop
    global uuid
    global categoryDescription
    print(req)
    loc_name = req['originalDetectIntentRequest']["payload"]["inputs"][0]["arguments"][0]["textValue"]
    if loc_name is None:
        loc_name = req['queryResult']['parameters']['locations']
    uuid = loc_dict[loc_dict["name"]==req['originalDetectIntentRequest']["payload"]["inputs"][0]["arguments"][0]["textValue"]]["uuid"].iloc[0]
    if categoryDescription=='':
        categoryDescription=loc_dict[loc_dict["uuid"]==uuid]["categoryDescription"]
    img = util.getImageUrl(cat_description[categoryDescription],uuid)
    name =loc_dict[loc_dict["uuid"]==uuid]["name"].iloc[0] 
    image = response.image(img[random.randint(0,len(img)-1)],name)
    description = util.getDescription(cat_description[categoryDescription],uuid)
    isOpen = util.isOpen(cat_description[categoryDescription],uuid)
    if isOpen:
        isOpen = "Open"
    else:
        isOpen = "Closed"
    description = description + "  \n"+"_Currently:"+isOpen+"_"
    rating = loc_dict[loc_dict["uuid"]==uuid]["rating"].iloc[0] 
    rating = "Rated:"+str(rating)
    card = response.createCard(name,description,image,subtitle = rating)
    
    sug = response.suggesstions(loc_prop[:7])
    resp = response.respButtonSuggestion(card,f"Nice choice, Let's search {name}","Would you like to know more?",sug)
    print(resp)
    return resp




def locationGetMoreInfo(req):
    global loc_prop
    if "Get More Info" in loc_prop:
        loc_prop.remove("Get More Info")
    print(req)
    sug = response.suggesstions(loc_prop[:7])
    global uuid
    global categoryDescription
    body = util.getDescription(cat_description[categoryDescription],uuid)
    body = util.getBody(cat_description[categoryDescription],uuid)
    singAward= util.getAwards(cat_description[categoryDescription],uuid)
    if singAward!='' or singAward is not None:
        body.append(f"{loc_dict[loc_dict['uuid']==uuid]['name'].iloc[0]}, is awarded with Singapore Tourism Award for best tourist place")
    b = body.pop(random.randint(0,len(body)-1))
    resp = response.responseSuggestions(f"Did you know?\n {b}",sug)
    return resp

def locationNameGetReview():
    global loc_prop
    global uuid
    global categoryDescription
    if "Reviews" in loc_prop:
        loc_prop.remove("Reviews")
    sug = response.suggesstions(loc_prop[:7])
    review = util.getReviewList(cat_description[categoryDescription],uuid)
    if review:
        review = review[random.randint(0,len(review)-1)]
        desc = "Here is what "+review["authorName"]+" says:\n"
        desc = desc + "Rated:"+str(review["rating"])+" stars"+"\n"
        desc = desc +  review["text"]+"\n"
    else:
        desc = "Be the first to Review the place..."
    resp = response.responseSuggestions(f"{desc}",sug)
    return resp
    
def locationNameNearestMrt():
    global loc_prop
    global uuid
    global categoryDescription
    if "Nearest MRT" in loc_prop:
        loc_prop.remove("Nearest MRT")
    sug = response.suggesstions(loc_prop[:7])
    mrt = util.getMrt(cat_description[categoryDescription],uuid)
    desc = "There are currently no MRTs near this location"
    if mrt:
        if len(mrt)==1:
            desc=f"Nearest MRT to {loc_dict[loc_dict['uuid']==uuid]['name'].iloc[0]} is "
            for i in range(len(mrt)):
                desc =desc+"\n" f"{mrt[i]}"
        else:
            desc=f"Nearest MRT to {loc_dict[loc_dict['uuid']==uuid]['name'].iloc[0]} are"
            for i in range(len(mrt)):
                desc =desc+"\n" f"{mrt[i]}"
    resp = response.responseSuggestions(f"{desc}",sug)
    return resp     
   
def locationNamegetOpenTime():
    global loc_prop
    global uuid
    global categoryDescription
    if "Open Time" in loc_prop:
        loc_prop.remove("Open Time")
    sug = response.suggesstions(loc_prop[:7])
    desc = "It would open soon"
    if util.getOpeningTime(cat_description[categoryDescription],uuid):
        openT = util.getOpeningTime(cat_description[categoryDescription],uuid)
        desc = f"{loc_dict[loc_dict['uuid']==uuid]['name'].iloc[0]} opens at {openT}"
    resp = response.responseSuggestions(f"{desc}",sug)
    return resp

def locationNameClosingTime():
    global uuid
    global categoryDescription
    global loc_prop
    if "Close Time" in loc_prop:
        loc_prop.remove("Close Time")
    sug = response.suggesstions(loc_prop[:7])
    desc = "The place would close in the evening"
    if util.getClosingTime(cat_description[categoryDescription],uuid):
        closeT = util.getClosingTime(cat_description[categoryDescription],uuid)
        desc = f"{loc_dict[loc_dict['uuid']==uuid]['name'].iloc[0]} closes at {closeT}"
    resp = response.responseSuggestions(f"{desc}",sug)
    return resp


def locationNameisOpen():
    global uuid
    global categoryDescription
    global loc_prop
    if "Is Open" in loc_prop:
        loc_prop.remove("Is Open")
    isOpen = util.isOpen(cat_description[categoryDescription],uuid)
    desc = ""
    if isOpen:
        timeToClose = util.timeToClose(cat_description[categoryDescription],uuid)
        desc = f"Its open currently and will close in {timeToClose}"
        print(desc)
    else:
        if util.nextOpen(cat_description[categoryDescription],uuid):
            desc = "Sorry its currently closed "+util.nextOpen(cat_description[categoryDescription],uuid)
            print(desc)
        else:
            desc = "Its currently closed but it would be open soon!!"
    sug = response.suggesstions(loc_prop[:7])
    resp = response.responseSuggestions(f"{desc}",sug)
    return resp    
     
def locationNameAddress():
    global uuid
    global categoryDescription
    global loc_prop
    if "How to get there" in loc_prop:
        loc_prop.remove("How to get there")
    Address = util.getAddress(cat_description[categoryDescription],uuid)
    desc = "Its located at \n"+Address
    img = util.getImageUrl(cat_description[categoryDescription],uuid)
    name =loc_dict[loc_dict["uuid"]==uuid]["name"].iloc[0] 
    image = response.image(img[random.randint(0,len(img)-1)],name)
    txt2 = "Would you like to see places nearby?"
    #lat = loc_dict[loc_dict["uuid"]==uuid]["lat"].iloc[0]
    #lng = loc_dict[loc_dict["uuid"]==uuid]["lng"].iloc[0]
    #w = weather.getWeather(lat,lng)
    #sug = ["Places near by"]
    url = util.getWebsite(cat_description[categoryDescription],uuid)
    button = response.buttons("Visit Them",url)
    card = response.createCard(name,desc,image,button)
    resp= response.responseCard("Below are the Address and Site details",txt2,card)
    print(resp)
    return resp


def locationNamegetPrice():
    global uuid
    global categoryDescription
    global priceC
    global priceA
    global priceS  
    global priceO
    resp = {}
    global loc_prop
    if "Get Fare" in loc_prop:
        loc_prop.remove("Get Fare")
    ticketed = util.getTicketed(cat_description[categoryDescription],uuid)
    if not ticketed:
        sug = response.suggesstions(loc_prop[:7])
        resp = response.responseSuggestions(f"Entry to {loc_dict[loc_dict['uuid']==uuid]['name'].iloc[0]} is free",sug)
    else: 
        if util.getPrice(cat_description[categoryDescription],uuid):
            [priceC,priceA,priceS,priceO]=util.getPrice(cat_description[categoryDescription],uuid)
            if priceC!='':
                print(util.getPrice(cat_description[categoryDescription],uuid))
                if priceC.replace(".","").isdigit():
                    priceC=float(priceC)
                    if priceA=='':
                        priceA=priceC
                    priceA=float(priceA)
                    sug = response.suggesstions(["Yes","No"])
                    resp = response.responseSuggestions(f"Would you like to share details about number of travellers with you?",sug)
                else:    
                    sug = response.suggesstions(loc_prop[:7])
                    resp = response.responseSuggestions(f"{priceC}",sug)
            else:
                sug = response.suggesstions(loc_prop[:7])
                resp = response.responseSuggestions(f"Admission rates of {loc_dict[loc_dict['uuid']==uuid]['name'].iloc[0]} has recently changed.Details for the same can be checked by their management",sug)
                    
        else:
            sug = response.suggesstions(loc_prop[:7])
            resp = response.responseSuggestions(f"Entry to {loc_dict[loc_dict['uuid']==uuid]['name'].iloc[0]} is free",sug)
    print(resp)
    return resp  


def locationNamegetPriceno():
    global priceC
    global priceA
    global priceS  
    global priceO
    global loc_dic
    desc = "Here are the ticket price:\n"
    desc += "Adult:S$"+str(priceA)+"\n"
    desc += "Child:S$"+str(priceC)+"\n"
    print(desc)
    sug = response.suggesstions(loc_prop[:7])
    resp = response.responseSuggestions(desc,sug) 
    print(resp)
    return resp
    
def locationNamegetPriceyes():
    sug = ["One","Two","Three","Four"]
    sug = response.suggesstions(sug)
    resp = response.responseSuggestions(f"How many adults are travelling with you?",sug)
    return resp

def locationNamegetPriceAdults(req):
    global number_adults
    print(req)
    number_adults = float(req['queryResult']['parameters']['number'])
    sug = ["One","Two","Three","Four"]
    sug = response.suggesstions(sug)
    resp = response.responseSuggestions(f"...and how many children?",sug)
    return resp
    
def locationNamegetPriceChildren(req):
    global number_adults
    global number_children
    global priceC
    global priceA
    global loc_dict
    print(priceA)
    print(priceC)
    if number_adults=='':
        number_adults=0
    if number_children=='':
        number_children=0
        
    number_children = int(req['queryResult']['parameters']['number'])
    print(number_children)
    desc  = "It would be a total of:  \n"
    desc  = desc + "Adults:S$"+ str(priceA*number_adults)+"\n"
    desc  = desc + "Children:S$"+ str(priceC*number_children)+"\n"
    desc  = desc + "Total:S$"+str(priceA*number_adults+priceC*number_children)
    sug = response.suggesstions(loc_prop[:7])
    resp = response.responseSuggestions(desc,sug)
    print(resp)
    return resp

def locationNameAddressyes():
    global name
    global user_lat
    global user_lgn
    global uuid
    global categoryDescription
    global number_adults
    global number_children
    global occassion
    global tags
    global loc_prop
    loc_prop =''
    name=loc_dict[loc_dict["uuid"]==uuid]["name"].iloc[0]
    user_lat=float(loc_dict[loc_dict["uuid"]==uuid]["lat"].iloc[0])
    user_lgn=float(loc_dict[loc_dict["uuid"]==uuid]["lng"].iloc[0])
    tags = ''
    uuid =''
    occassion=''
    categoryDescription=''
    number_adults=''
    number_children=''
    sug = response.suggesstions(["Shopping","Find Food","Attractions","Bars & Clubs"])
    resp = response.responseSuggestions("What would you like to do?",sug)
    return resp

def getCusine():
    global uuid
    global loc_prop
    cusine = loc_dict[loc_dict["uuid"]==uuid]["cusine"].iloc[0]
    cusine = cusine.split(',')
    print(cusine)
    desc = f"{loc_dict[loc_dict['uuid']==uuid]['name'].iloc[0]} specializes in:\n"
    for i in range(len(cusine)):
        desc+=f"{i+1}. {cusine[i]}\n"
    sug = response.suggesstions(loc_prop[:7])
    resp = response.responseSuggestions(desc,sug)
    return resp
    
def locationNameLike():
    global occassion
    global tags
    global cusine
    global user_lat
    global user_lgn
    global categoryDescription
    global name
    if user_lat=='' or user_lgn=='' or user_lat is None or user_lgn is None:
        user_lat = None
        user_lgn = None
    if occassion!='':
        d=findlocations.getEntity(categoryDescription=categoryDescription,types=occassion,lat=user_lat,lng=user_lgn)
    elif tags!='':
        d=findlocations.getEntity(categoryDescription=categoryDescription,tag=tags,lat=user_lat,lng=user_lgn)
    elif cusine!='':
        d=findlocations.getEntity(categoryDescription=categoryDescription,cusine=cusine,lat=user_lat,lng=user_lgn)
    if len(d)<=1:
        findlocations.utilreset()
        if occassion!='':
            d=findlocations.getEntity(categoryDescription=categoryDescription,types=occassion,lat=user_lat,lng=user_lgn)
        elif tags!='':
            d=findlocations.getEntity(categoryDescription=categoryDescription,tag=tags,lat=user_lat,lng=user_lgn)
        elif cusine!='':
            d=findlocations.getEntity(categoryDescription=categoryDescription,cusine=cusine,lat=user_lat,lng=user_lgn) 
    names = []
    image=''
    carousel=[]
    Distance = []
    setloc_prop()
    for i in d:
        names.append(str(loc_dict[loc_dict["uuid"]==i]["name"].iloc[0]))
    if user_lat and user_lgn:
        desc = "Here are few places of your interest"
        for i in d:
            lat = float(loc_dict[loc_dict["uuid"]==i]["lat"].iloc[0])
            lgn = float(loc_dict[loc_dict["uuid"]==i]["lng"].iloc[0])
            dis= loc.find_distance(float(user_lat),float(user_lgn),float(lat),float(lgn))
            if dis>=1000:
                dis = round(dis/1000,2)
                dis = "Distance:"+str(dis) + " kms"
            else:
                dis = round(dis,2)
                dis = "Distance:"+str(dis) +" mts"
            Distance.append(dis)
    else:
         desc= "Here are some top rated place of your interest"
         for i in d:
            rating = loc_dict[loc_dict["uuid"]==i]["rating"].iloc[0]
            rating = "Rated:"+str(rating)+" stars"
            Distance.append(rating)
    for i in range(len(d)):
        img=util.getImageUrl(cat_description[categoryDescription],d[i])
        if img is None:
            carousel.append(response.createCarouselWImage(names[i],names[i]))
        else:    
            image=(response.image(img[0],names[i]))
            carousel.append(response.createCarouselDesc(names[i],image,Distance[i],names[i]))
    sug = response.suggesstions(["Show Similar Places","Show Different Places"])        
    req = response.respCarouselS(carousel,desc,sug)
    print(req)
    return req

def attractionyes():
    sug = response.suggesstions(["Local","Indian","Chinese","Japanese"])        
    resp = response.responseSuggestions("Are you looking for some specific dish or cusine?",sug)
    return resp

def attractionno():
    sug = response.suggesstions(restuarant_type)        
    resp = response.responseSuggestions("Where would you like to go?",sug)
    print(resp)
    return resp

def restaurantCusine(req):
    global cusine
    global categoryDescription
    global occassion
    occassion = ''
    cusine=req['queryResult']['parameters']['cusine']
    resp = locationNameLike()
    return resp

def locationNameDiff():
    global occassion
    global attraction_type
    global bars_type
    global restuarant_type
    global malls_type
    global cusine
    cusine =''
    oc = None
    if occassion !='':
        oc = occassion
    remove_type(oc)
    occassion=''
    findlocations.utilreset()
    if categoryDescription=="Attractions":
        sug = response.suggesstions(attraction_type)
    elif categoryDescription=="Bars & Clubs":
        sug = response.suggesstions(bars_type)
    elif categoryDescription=="Food & Beverages":    
        sug = response.suggesstions(restuarant_type)
    elif categoryDescription=="Malls & Shops":
        sug = response.suggesstions(malls_type)
    setloc_prop()
    print(loc_prop)
    if categoryDescription=="Food & Beverages":
        sug = response.suggesstions(["Yes","No"])
        resp = response.responseSuggestions(f"Are you looking for some specific cusine?",sug)
    else:    
        resp=response.responseSuggestions(f"Which kind of activity are you currently interested in?",sug)
    return resp
    
def locationCat(req):
    global categoryDescription
    global user_lat
    global user_lgn
    reset_all()
    loc_name = req['queryResult']['parameters']['loc']
    categoryDescription=req['queryResult']['parameters']['categoryDescription']
    categoryDescription=categoryDescription.title()
    print(loc_name+" "+categoryDescription)
    if loc_name=="near me" and (user_lat=='' or user_lgn==''):
        resp = response.permissions(["DEVICE_PRECISE_LOCATION"],"Can we know your location?")
    else:
        user_lat,user_lgn = getloc.getlatlong(loc_name)
        print(user_lat,user_lgn)
        if categoryDescription=="Attractions":
            sug = response.suggesstions(["Adventure","Arts","History & Culture","Leisure & Recreation","Nature & WildLife","Others"])
        elif categoryDescription=="Bars & Clubs":
            sug = response.suggesstions(bars_type)
        elif categoryDescription=="Food & Beverages":    
            sug = response.suggesstions(restuarant_type)
        elif categoryDescription=="Malls & Shops":
            sug = response.suggesstions(malls_type)
        setloc_prop()
        if categoryDescription=="Food & Beverages":
            sug = response.suggesstions(["Yes","No"])
            resp = response.responseSuggestions(f"Are you looking for some specific cusine?",sug)
        else: 
            resp=response.responseSuggestions(f"Which kind of activity are you currently interested in?",sug)
    return resp    

def actions_intent_CANCEL():
    reset_all()
    resp = response.simpleResponse("Bye!!. Let me know when we can look for places in Singapore",False)
    return resp
    

app = Flask(__name__)



@app.route("/",methods=["POST"])
def main():
    global name
    resp={}
    req = request.get_json()
    intent = req['queryResult']['intent']['displayName']
    print(intent)
    if intent=="Default Welcome Intent":
        resp = DefaultWelcome()
    if intent=="action_intent_PERMISSION":
        resp = actions_intent_PERMISSION(req)
    if intent == "metBefore":
        resp = metBefore()
    if intent == "knowMore":
        print("Inside Know more!!")
        resp=knowMore()
        print(resp)
    if intent == "nearMe":
        resp=nearMe()
    if intent == "attraction":
        resp = attraction(req)
    if intent=="attractionType" or intent=="LocationOthertype" or intent=="LocationCattype":
        resp = attractionTypes(req)
    if intent=="locationName":
        resp = locationName(req)
    if intent=="Location-getMoreInfo":
        resp = locationGetMoreInfo(req)
    if intent == "locationNameGetReview":
        resp = locationNameGetReview()
    if intent == "locationNameNearestMrt":
        resp = locationNameNearestMrt()
    if intent =="locationName-getOpenTime":
        resp = locationNamegetOpenTime()
    if intent == "locationName - ClosingTime":
        resp = locationNameClosingTime()
    if intent == "locationName - getPrice":
        resp = locationNamegetPrice()
    if intent == "locationNamegetPriceyes":
        resp = locationNamegetPriceyes()
    if intent == "locationName - getPrice - no":
        resp = locationNamegetPriceno()    
    if intent == "locationName - getPrice - select.numberAdults":
        resp = locationNamegetPriceAdults(req)
    if intent == "locationNamegetPriceChildren":
        resp = locationNamegetPriceChildren(req)
    if intent == "locationName - isOpen":
        resp = locationNameisOpen()
    if intent == "locationNameAddress":
        resp = locationNameAddress()
    if intent == "RestaurantCusine":
        resp = restaurantCusine(req)
    if intent == "locationNameAddress - yes":
        resp = locationNameAddressyes()
    if intent == "locationName - cusine":
        resp = getCusine()    
    if intent == "locationNameLike":
        resp = locationNameLike()
    if intent == "attraction - yes" or intent=="LocationOther - yes" or intent=="LocationCat - yes":
        resp = attractionyes()      
    if intent == "attraction - no" or intent=="LocationOther - no" or intent=="LocationCat - no":
        resp = attractionno()
    if intent == "LocationOther":
        resp = locationNameDiff()
    if intent == "LocationCat":
        resp = locationCat(req)
    if intent == "actions_intent_CANCEL":
        resp = actions_intent_CANCEL()
    
    return Response(json.dumps(resp), status=200, content_type="application/json")
    
    
