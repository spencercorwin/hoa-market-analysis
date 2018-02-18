#! /usr/bin/env python3

#Onboard API Test

import requests, os, bs4

ZWSID = 'X1-ZWz18s1gn1k8i3_4pyss'
address = '2184 Canyon Dr'
zipCode = '92627'

def getSearchResults(address, zipCode, ZWSID):
    url = 'http://www.zillow.com/webservice/GetSearchResults.htm?zws-id={}&address={}&citystatezip={}'.format(ZWSID,address,zipCode)
    response = requests.get(url)
    response.raise_for_status()
    data = bs4.BeautifulSoup(response.text, 'lxml')
    elems = data.select('zpid')
    return (elems[0].getText())
