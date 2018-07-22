
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

#Get property details from Zillow property ID
def getUpdatedPropertyDetails(ZWSID, ZPID): #THIS FUNCTION NEEDS WORK
    url = 'http://www.zillow.com/webserive/GetUpdatedPropertyDetails.htm?zws-id={}&zpid={}'.format(ZWSID,ZPID)
    response = requests.get(url)
    response.raise_for_status
    data = bs4.BeautifulSoup(response.text, 'lxml')
    beds = data.select('bedrooms')[0].getText()
    baths = data.select('bathrooms')[0].getText()
    SF = data.select('finishedSqFt')[0].getText()


#Get Zillow Property ID and comp data for the given address to search
ZPID = getSearchResults(address, zipCode, ZWSID)
allData = getDeepComps(ZWSID,ZPID,numOfComps)
