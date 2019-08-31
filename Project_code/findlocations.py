#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Aug 22 14:54:33 2019

@author: shashanknigam
"""

import pandas as pd 
import loc
import app
util_seen = []
def utilreset():
    global util_seen
    util_seen = []

def getEntity(categoryDescription=None,cusine=None,types=None,tag=None,lat=None,lng=None,distance=None):
    print(f"{categoryDescription} {cusine} {types} {tag} {lat} {lng} {distance}")
    global util_seen
    print(util_seen)
    if len(util_seen)>20:
        utilreset()
    col=''
    indexes=[]
    loc_dict_temp={}
    distance=[]
    index_dist=[]
    if categoryDescription:
        loc_dict_temp = app.loc_dict[app.loc_dict["categoryDescription"]==categoryDescription]
        if types:
            col="type"
            for i in range(len(loc_dict_temp)):
                if not pd.isna(loc_dict_temp[col].iloc[i]):
                    if types in loc_dict_temp[col].iloc[i]:
                        if loc_dict_temp["uuid"].iloc[i] not in util_seen:
                            indexes.append(int(loc_dict_temp["rownum"].iloc[i]))
            loc_dict_temp=app.loc_dict.iloc[indexes]
            print("type")
            print(loc_dict_temp)
            indexes=[]
        if cusine:
            col = "cusine"            
            for i in range(len(loc_dict_temp)):
                if not pd.isna(loc_dict_temp[col].iloc[i]):
                    if cusine in loc_dict_temp[col].iloc[i]:
                        if loc_dict_temp["uuid"].iloc[i] not in util_seen:
                            indexes.append(int(loc_dict_temp["rownum"].iloc[i]))
            loc_dict_temp=app.loc_dict.iloc[indexes]
            print("cusine")
            print(loc_dict_temp)
            indexes=[]
        if tag:
            for i in range(len(loc_dict_temp)):
                if not pd.isna(loc_dict_temp["tags"].iloc[i]):
                    if tag in loc_dict_temp["tags"].iloc[i]:
                        if loc_dict_temp["uuid"].iloc[i] not in util_seen:
                            indexes.append(int(loc_dict_temp["rownum"].iloc[i]))
            loc_dict_temp=app.loc_dict.iloc[indexes]  
            indexes=[]
        if lat and lng:
            print(loc_dict_temp)
            for i in range(len(loc_dict_temp)):
                distance.insert(i,loc.find_distance(lat,lng,loc_dict_temp["lat"].iloc[i],loc_dict_temp["lng"].iloc[i]))
            print(distance)
            print(util_seen)
            if len(distance)>3:
                for x in range(len(distance)):
                    
                    minDis = distance.index(min(distance))
                    print(minDis)
                    print(loc_dict_temp["uuid"].iloc[minDis])
                    if distance[minDis]!=0 and loc_dict_temp["uuid"].iloc[minDis] not in util_seen:
                        index_dist.append(loc_dict_temp["rownum"].iloc[minDis])
                        print(index_dist)
                    print(distance[minDis])    
                    distance[minDis] =9999999999
            else:
                for x in range(len(distance)):
                    
                    minDis = distance.index(min(distance))
                    if distance[minDis]!=0:
                        index_dist.append(loc_dict_temp["rownum"].iloc[minDis])
                        print(index_dist)
                    print(distance[minDis])    
                    distance[minDis] =9999999999
            loc_dict_temp = app.loc_dict.iloc[index_dist]
            indexes = loc_dict_temp.index
            print(indexes)
            print(util_seen)
            length = len(indexes)
            if length>3:
                length=3
            for x1 in range(length):
                if loc_dict_temp["uuid"][indexes[x1]] not in util_seen:
                    util_seen.append(loc_dict_temp["uuid"][indexes[x1]])
            print(loc_dict_temp)        
            return list(loc_dict_temp["uuid"].head(n=2))    
        else:
            indexes = loc_dict_temp.index
            print(indexes)
            length = len(indexes)
            if length>2:
                length=2
            for x1 in range(length):
                if loc_dict_temp["uuid"][indexes[x1]] not in util_seen:
                    print(loc_dict_temp["uuid"][indexes[x1]])
                    util_seen.append(loc_dict_temp["uuid"][indexes[x1]])
            return list(loc_dict_temp["uuid"].head(n=2))
    else:
         for i in range(len(app.loc_dict)):
                distance.insert(i,loc.find_distance(lat,lng,loc_dict_temp["lat"].iloc[i],loc_dict_temp["lng"].iloc[i]))
         for x in range(10):
             minDis = distance.index(min(distance))
             if distance[minDis]!=0 and loc_dict_temp["uuid"].iloc[minDis] not in util_seen:
                 index_dist.append(loc_dict_temp["rownum"].iloc[minDis])
             distance[minDis] =9999999999             
         loc_dict_temp=app.loc_dict.iloc(index_dist)
         indexes = loc_dict_temp.index
         length = len(indexes)
         if length>3:
                length=3
         for x1 in range(length):
             if loc_dict_temp["uuid"][indexes[x1]] not in util_seen:
                 util_seen.append(loc_dict_temp["uuid"][indexes[x1]])
         return list(loc_dict_temp["uuid"].head(n=2))