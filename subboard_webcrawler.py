import pymysql
from lxml import html
import requests
from lxml import etree

for lis in range(7520, 6700, -1):
    url = 'http://subboard.com/och/listing.asp?id=%s'%lis
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
    with open('C:\\Users\\Sathish\\Dropbox\\apt_search\\listing_all.csv', 'a') as the_file:
        if ("6" in lease or "5" in lease or "7" or "12" in lease):
            rent = tree.xpath('//dt[text()="Rent"]/following-sibling::dd/div/text()')
            location = tree.xpath('//*[@id="content"]/dl/dd[1]/text()')
            row = ''
            #print url
            row+=url+'|'
            #print 'location', location[0].replace('\r\n\t\t\t\t\t','')+','+location[1]
            row+=location[0].replace('\r\n\t\t\t\t\t','')+', '+location[1]+'|'
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
            the_file.write(row)
            print '***************************'
        else:
            availability
        

    
    
    #print lease
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
    
    
        
    


