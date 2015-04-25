import pymysql
from lxml import html
import requests
from lxml import etree

for lis in range(7493, 6700, -1):
    url = 'http://subboard.com/och/listing.asp?id=%s'%lis
    page = requests.get(url)
    #print page.text.tostring()
    #print page
    tree = html.fromstring(page.text)
    pagetext = etree.tostring(tree)
    if "/och/listing.asp" in pagetext :
        continue
        
    
    #e = root.xpath('.//a[text()="TEXT A"]')
    lease = tree.xpath('//dt[text()="Lease"]/following-sibling::*/text()')[0]
    #print lease
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
        
    

