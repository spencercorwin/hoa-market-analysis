#! /usr/bin/env python3

#Zillow API test

import requests, os, bs4

ZWSID = #Zillow API ID here
address = '2184 Canyon Dr'
zipCode = '92627'

#Use this to get a Zillow Property ID
def getSearchResults(address, zipCode, ZWSID):
    url = 'http://www.zillow.com/webservice/GetSearchResults.htm?zws-id={}&address={}&citystatezip={}'.format(ZWSID,address,zipCode)
    response = requests.get(url)
    response.raise_for_status()
    data = bs4.BeautifulSoup(response.text, 'lxml')
    elems = data.select('zpid')
    return (elems[0].getText())

#Get the Zestimate for a property with the Zillow Property ID
def getZestimate(ZWSID, ZPID):
    url = 'http://www.zillow.com/webservice/GetZestimate.htm?zws-id={}&zpid={}'.format(ZWSID,ZPID)
    response = requests.get(url)
    response.raise_for_status()
    data = bs4.BeautifulSoup(response.text, 'lxml')
    elems = data.select('zestimate amount')
    return (elems[0].getText())

#Function to get the comps and comp details from an inputed Zillow Property ID
def getDeepComps(ZWSID, ZPID, numOfComps):
    url = 'http://www.zillow.com/webservice/GetDeepComps.htm?zws-id={}&zpid={}&count={}'.format(ZWSID,ZPID,numOfComps)
    response = requests.get(url)
    response.raise_for_status()
    data = bs4.BeautifulSoup(response.text, 'lxml')
    allData = {}
    for i in range(numOfComps):
        allData[i] = {}
    for i in range(numOfComps):
        address = data.select('street')[i].getText()
        allData[i]['Address'] = address
        beds = data.select('bedrooms')[i].getText()
        allData[i]['Beds'] = beds
        baths = data.select('bathrooms')[i].getText()
        allData[i]['Baths'] = baths
        SF = data.select('finishedsqft')[i].getText()
        allData[i]['SF'] = SF
        lastSoldPrice = data.select('lastsoldprice')[i].getText()
        allData[i]['Sale Price'] = lastSoldPrice
        lastSoldDate = data.select('lastsolddate')[i].getText()
        allData[i]['Sale Date'] = lastSoldDate
        zestimate = data.select('zestimate amount')[i].getText()
        allData[i]['Zestimate'] = zestimate
    print (allData)

"""    for i in range(0,len(allData),7):
        print('Address:'+allData[i])
        print('SF:'+allData[i+1])

    for i in range(numOfComps):
        print ('Address:'+propAddress[i].getText())
        print ('SF:'+SF[i].getText())
        print ('Beds:'+beds[i].getText())
        print ('Baths:'+baths[i].getText())
        print ('Last Sold Price:'+lastSoldPrice[i].getText())
        print ('Last Sold Date:'+lastSoldDate[i].getText())
        print ('Zestimate:'+zestimate[i].getText())"""

ZPID = getSearchResults(address, zipCode, ZWSID)
getDeepComps(ZWSID,ZPID,2)
