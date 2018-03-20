#! /usr/bin/env python3

import http.client
import json

API_key = #Insert Onboard API here
address1 = '2184%20Canyon%20Dr'
address2 = 'Costa%20Mesa%2CCA'
radius = '0.06'
page = '1'
pagesize ='2'


#Use this to get all the properties in the area. Get their addresses and property IDs
def get_Onboard_properties_from_address(API_key, address1, address2, radius, page, pagesize):
    conn = http.client.HTTPSConnection("search.onboard-apis.com")
    headers = {'accept': "application/json",'apikey': API_key}
    conn.request("GET", "/propertyapi/v1.0.0/property/address?address1={}&address2={}&radius={}&page={}&pagesize={}".format(address1,address2,radius,page,pagesize), headers=headers) 
    res = conn.getresponse() 
    data = res.read()
    json_data = json.loads(data)
    properties = json_data['property']
    for i in range(len(properties)):
        print (properties[i]['address']['oneLine'])    #gives the address
        print (properties[i]['address']['line1'] #gives address line 1
        print (properties[i]['address']['line2'] #gives address line 2
        print (properties[i]['identifier']['obPropId']) #gives the Onboard property ID


#Use this to get sales history for each address
def get_prop_data_sales_history_from_address(API_key, address1, address2):
    conn = http.client.HTTPSConnection("search.onboard-apis.com")
    headers = {'accept': "application/json",'apikey': API_key}
    conn.request("GET", "/propertyapi/v1.0.0/saleshistory/detail?address1={}&address2={}".format(address1, address2), headers=headers) 
    res = conn.getresponse() 
    data = res.read()
    json_data = json.loads(data)
    properties = json_data['property']
    for i in range(len(properties)):
        print (properties[i]['building']['size']['bldgsize'])    #gives building size
        print (properties[i]['building']['rooms']['beds']) #gives the number of beds
        print (properties[i]['building']['rooms']['bathstotal']) #gives the number of baths
        print (properties[i]['salehistory'][0]['amount']['saleamt']) #gives the most recent sales amount
        print (properties[i]['salehistory'][0]['amount']['salerecdate']) #gives the most recent sale date
        print (properties[i]['salehistory'][1]['amount']['saleamt']) #gives the next most recent sales amount
        print (properties[i]['salehistory'][1]['amount']['salerecdate']) #gives the next most recent sales amount




#get_Onboard_properties_from_address(API_key, address1, address2, radius, page, pagesize)
get_prop_data_sales_history_from_address(API_key, address1, address2)
