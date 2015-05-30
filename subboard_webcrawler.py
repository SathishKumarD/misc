import pymysql
from lxml import html
import requests
from lxml import etree
import re
import json


#global constants
apikey=''  #your API key https://developers.google.com/maps/documentation/distancematrix/
busstops =['Main circle, Buffalo,NY' , 'Goodyear Hall, Buffalo,NY','Grover Cleveland Highway and Maynard Drive bus stop','Student Union Building, Putnam Way, Buffalo','Flint Loop, Buffalo, NY','Ellicott Complex, Buffalo, NY','Flint Road and UB Service Road, Amherst, NY']
mapsapiurl = 'https://maps.googleapis.com/maps/api/distancematrix/json?origins=[[origin]]&destinations=[[destination]]&mode=walking&key=[[apikey]]'
suboardurl ='http://subboard.com/och/listing.asp?id=%s'
listingStart,listingEnd = 7589, 7000


def sanitizeAddress(address):
    address = address.lower()
    stopwords =[',','.','apt','lower','upper','#']
    for s in stopwords:
        address =address.replace(s,'')
    address = re.sub(' +',' ',address)
    address = address.strip().replace(' ','+')
    return address
    
#get the walking distance, duration to the nearest busstop
def getWalkingDistanceToBusstop(originaddr):
    originaddr = sanitizeAddress(originaddr)
    
    print mapsapiurl.replace('[[origin]]',originaddr).replace('[[destination]]',sanitizeAddress(busstops[0]))
    mindis= 100000
    mindisstop ='Not Found'
    mindur =0
    for busstop in busstops:
        stop = sanitizeAddress(busstop)
        url = mapsapiurl.replace('[[origin]]',originaddr).replace('[[destination]]',stop).replace('[[apikey]]',apikey)
        #print url
        page = requests.get(url)
        #print page.text
        distancejson = json.loads(page.text)
        
         
        if distancejson['rows'][0]['elements'][0]['status'] == 'NOT_FOUND':
            print 'Cannot find distance'
            return str(mindis),mindisstop,mindur
        
        dis = distancejson['rows'][0]['elements'][0]['distance']['value']
        duration = int(distancejson['rows'][0]['elements'][0]['duration']['value'])/60
        dist = float(dis)*0.000621371
        #print busstop , dist,mindis, duration
        if dist < mindis:
            mindis = dist
            mindisstop = busstop
            mindur = duration
            
    
    mindis = '%.2f' %mindis
    #print mindis,mindisstop,mindur
    return mindis,mindisstop,mindur

for lis in range(listingStart, listingEnd, -1):
    url = suboardurl%lis
    page = requests.get(url)
    #print page.text.tostring()
    #print page
    tree = html.fromstring(page.text)
    pagetext = etree.tostring(tree)
    if "/och/listing.asp" in pagetext :
        continue
        
    #print url
    lease = tree.xpath('//dt[text()="Lease"]/following-sibling::*/text()')[0]
    Bedrooms = tree.xpath('//dt[text()="Bedrooms"]/following-sibling::*/text()')[0]
    availability = Bedrooms.split()
    
    #print availability
    with open('/Users/sathish/misc/listing_all.csv', 'a') as the_file:
        if ("6" in lease or "5" in lease or "7" or "12" in lease):
            rent = tree.xpath('//dt[text()="Rent"]/following-sibling::dd/div/text()')
            location = tree.xpath('//*[@id="content"]/dl/dd[1]/text()')
            row = ''
            #print url
            row+=url+'|'
            #print 'location', location[0].replace('\r\n\t\t\t\t\t','')+','+location[1]
            row+=location[0].replace('\r\n\t\t\t\t\t','')+', '+location[1]+'|'
            mindis,mindistop,duration = getWalkingDistanceToBusstop(location[0].replace('\r\n\t\t\t\t\t','')+', '+location[1])
            #print mindis,mindistop,duration
            
            row+=mindis +'|'
            row+=mindistop +'|'
            row+=str(duration) +'|'
            #print 'lease', lease
            row+=lease+'|'
            #print 'rent:' ,rent[0]
            row+=rent[0]+'|'
            #print 'contact:',rent[1]
            row+=rent[1]+'|'
            
            #print 'Phone:' ,rent[2]
            row+=rent[2]+'|'
            if len(rent) >3:
                #print 'Best time' , rent[3] 
                row+=rent[3]+'|'
                
            if len(rent) >4:
                #print 'email' , rent[4] 
                row+=rent[4]+'|'
            #print 'Bedrooms', Bedrooms
            row+=Bedrooms+'\n'
            
            ## windows machine hack revert it back
            row = row.replace(',','```')
            row = row.replace('|',',')
            
            ## hack ends
            
            the_file.write(row)
            print '***************************'
        else:
            availability
        

    
    
    #print lease - only 6 or 5 or 7 months lease
    """
    if "6" in lease or "5" in lease or "7" in lease:
        rent = tree.xpath('//dt[text()="Rent"]/following-sibling::dd/div/text()')
        Bedrooms = tree.xpath('//dt[text()="Bedrooms"]/following-sibling::*/text()')[0]
        print url
        print 'lease', lease
        print 'rent:' ,rent[0]
        print 'contact:',rent[1]
        print 'Phone:' ,rent[2]
        if len(rent) >3:
            print 'Best time' , rent[3] 
        if len(rent) >4:
            print 'email' , rent[4] 
        print 'Bedrooms', Bedrooms
        print '******************************' 
        """
    
    
        
    


