#! /usr/bin/env python3
"""This program will create a market analysis in a MS Word document from a
command line input of the city where the subject property is. This program
is used get basic market data for a subject city."""

import os, sys, json, requests, bs4, datetime, docx

os.chdir('/Users/spencercorwin/Desktop')

city = str(sys.argv[1:])        #get the subject city

#Get the JSON data from Data USA API


#Get the JSON data from BLS API


#Get data from Trulia


#Create new Word document
todaysDate = datetime.datetime.now()
todaysDateString = todaysDate.strftime('%m/%d/%y')  #get today's date in a nice format
doc = docx.Document()

#Add text to the document
doc.add_heading('Market Analysis:', 1)
doc.add_paragraph(
    '{} has a population of {} with a median age of {} and poverty rate of {}%.', style='ListBullet'
    )
doc.add_paragraph(
    'Median household income of {} and median property value of {}.', style='ListBullet'
    )
doc.add_paragraph(
    'Residents of {} work predominantly in {}, {}, {}, and {} positions.', style='ListBullet'
    )
doc.add_paragraph(
    'The highest paid jobs in {} by median earnings are in {}, {}, and {}.', style='ListBullet'
    )
doc.add_paragraph(
    '{}\' unemployment rate is {} according to the BLS.', style='ListBullet'
    )

#Add sources
doc.add_paragraph('Sourced '+todaysDateString+':')


#Save Word document on the Desktop
doc.save(city+' Market Analysis '+todaysDateString)
