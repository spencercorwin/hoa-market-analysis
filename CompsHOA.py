#! /usr/bin/env python3
"""This program will take an address as an input from the command line and
create an Excel file on the desktop with a specially formated table containing
comparable property sales in the area, complete with address, distance from
subject, price sold, date sold, price per SF, etc."""

import openpyxl, sys, os, json, requests, datetime, bs4
from openpyxl.styles import Font, PatternFill, Color
from openpyxl.utils import get_column_letter
from openpyxl.styles.borders import Border, Side

os.chdir('/Users/spencercorwin/Desktop')

ZWSID = #make sure to input your Zillow API ID here
address = '26162 La Real'
zipCode = '92691'
numOfComps = 25     #this is the max comps Zillow will give you

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
    allData = {}        #initializing the dictionary
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
    return (allData)

#Get Zillow Property ID and comp data for the given address to search
ZPID = getSearchResults(address, zipCode, ZWSID)
allData = getDeepComps(ZWSID,ZPID,numOfComps)

#Create Excel workbook on Desktop
todaysDate = datetime.datetime.now()
todaysDateString = todaysDate.strftime('%m.%d.%y')      #get today's date in a nice format
headingFontObj = Font(bold=True, size=11, name='Calibri', underline='single')
wb = openpyxl.Workbook()                #create workbook on Desktop with formatted name
sheet = wb.active
headingsList = ['Address','Mi from Subject','Beds', 'Baths','SF','Sale Price','Price/SF','Sale Date','Zestimate','Zestimate/SF','Prev Sale Price','Prev Sale Date','Appreciation']

#Fill in the row with data from allData returned from getDeepComps
for i in range(numOfComps):
    try:
        sheet.cell(row=i+2,column=1).value = allData[i]['Address']
        sheet.cell(row=i+2,column=3).value = int(allData[i]['Beds'])
        sheet.cell(row=i+2,column=4).value = float(allData[i]['Baths'])
        sheet.cell(row=i+2,column=5).value = int(allData[i]['SF'])
        sheet.cell(row=i+2,column=6).value = int(allData[i]['Sale Price'])
        sheet.cell(row=i+2,column=8).value = allData[i]['Sale Date']
        sheet.cell(row=i+2,column=9).value = int(allData[i]['Zestimate'])
    except:
        continue

#Fill in the header row with the headings from headingsList
for c in range(1,len(headingsList)+1):
    sheet.cell(row=1,column=c).value = headingsList[c-1]
    sheet.cell(row=1,column=c).font = headingFontObj

#Create formulas within the table
for r in range(2,numOfComps+2):
    sheet.cell(row=r,column=7).value = '=F'+str(r)+'/E'+str(r)
    sheet.cell(row=r,column=10).value = '=I'+str(r)+'/E'+str(r)
    sheet.cell(row=r,column=13).value = '=(F'+str(r)+'-K'+str(r)+')/K'+str(r)

#Create averages and totals at the bottom of the table
bottomFontObj = Font(bold=True, size=11, name='Calibri')
averagedColumns = [5,6,7,9,10]
avgRow = numOfComps+2
sheet.cell(row=avgRow,column=4).value = 'Averages:'
sheet.cell(row=avgRow,column=4).font = bottomFontObj
for c in averagedColumns:
    sheet.cell(row=avgRow,column=c).value = '=average({0}2:{0}{1})'.format(get_column_letter(c), numOfComps+1)
    sheet.cell(row=avgRow,column=c).font = bottomFontObj

#Create borders around all cells except the last row
borderObj = Border(left=Side(style='thin'),right=Side(style='thin'),top=Side(style='thin'),bottom=Side(style='thin'))
for c in range(1,sheet.max_column+1):
    for r in range(1,sheet.max_row):
        sheet.cell(row=r,column=c).border = borderObj

#Fill cells with white color
whiteFill = PatternFill('solid',fgColor='00FFFFFF')
for c in range(1,sheet.max_column+1):
    for r in range(1,sheet.max_row+1):
        sheet.cell(row=r,column=c).fill = whiteFill

#Resize columns
for c in range(1,sheet.max_column):
    max_length = len(str(sheet.cell(row=1,column=c).value))
    for r in range(1,sheet.max_row):
        try:
            if len(str(sheet.cell(row=r,column=c).value)) > max_length:
                max_length = len(str(sheet.cell(row=r,column=c).value))
        except:
            continue
    sheet.column_dimensions[get_column_letter(c)].width = max_length
    
#Save and close the file with a formatted name
wb.save(address+' Comps '+todaysDateString+'.xlsx')
print('I\'ve done your bidding, human.')
