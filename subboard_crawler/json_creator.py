
# coding: utf-8

# In[39]:

import sys

file = open('/Users/sathish/misc/subboard_crawler/listing_all.csv')

from random import randint

import re

import json
import re
import requests

mapsapiurl = 'https://maps.googleapis.com/maps/api/geocode/json?address=[[origin]]'

def sanitizeAddress2(address):
    address = address.lower()
    stopwords =[',','.','apt','lower','upper','#']
    for s in stopwords:
        address =address.replace(s,'')
    address = address.strip()
    address = re.sub('```','',address)   
    address = address.strip().replace(' ','+')
    return address

def getLattitude(originaddr):
    originaddr = sanitizeAddress2(originaddr)
    url = mapsapiurl.replace('[[origin]]',originaddr)    
    page = requests.get(url)
    pagejson = json.loads(page.text)
    #print(pagejson)
    lattitude = pagejson['results'][0]['geometry']['location']['lat']
    longitude = pagejson['results'][0]['geometry']['location']['lng']
    lat=lattitude
    longi= longitude
    return lat,longi

def sanitizeAddress(address):
    address = address.replace('```','')
    #print address
    address = address.lower()
    stopwords =[',','.','apt','lower','upper','#']
    for s in stopwords:
        address =address.replace(s,'')
    address = re.sub(' +',' ',address)
    #address = address.strip().replace(' ','+')
    alist = address.split()
    d={}
    d['number'] = alist[0]
    d['zipcode'] = alist[len(alist)-1]
    d['state'] = alist[len(alist)-2].upper()
    d['city'] = ''.join([i for i in alist[len(alist)-3] if not i.isdigit()]).capitalize()  
    d['address_1'] = ' '.join(alist[1:3]).capitalize()
    d['full_address'] = ', '.join([d['number'], d['address_1'],d['city'],d['state'],d['zipcode']])
    return d

jsonlist = []
houseId = 1

counter = 0
try:
    for line in file:
        counter+=1
        
        if counter >100:
            break
            
        #print line
        house = {}
        columns = line.split(',')
        house['address'] = sanitizeAddress(columns[1])
        house['busstop_distance'] = columns[2]
        house['busstop'] = columns[3].replace('```',"").replace('Buffalo',"").replace('NY',"").strip()
        house['busstop_walking_time'] = columns[4]
        
        house["overallBedbugRating"]= randint(1,5)
        house["overallLandlordRating"]= randint(1,5)
        house["overallrentRating"]= randint(1,5)
       

        ratings = []
        rating = {
        "bedbugRating": randint(1,5),
        "landlordRating": randint(1,5),
        "rentRating": randint(1,5),
        "comments": "Wow awesome machi!!"
       }


        ratings.append(rating)
        house['ratings'] = ratings


        lat,lng = getLattitude(columns[1])
        print lat,lng
        house["location"]= {"lat": lat,"lng": lng}
        house["houseId"] = houseId

        jsonlist.append(house)
        houseId+=1
        print k
except :
    print "Unexpected error:", sys.exc_info()[0]
    pass

    

filew = open('/Users/sathish/misc/subboard_crawler/listing.json','w')
pjson = str(jsonlist)
ojson = pjson.replace("'","\"")
filew.write(ojson)
print 'done'

    
    
    


# In[ ]:



