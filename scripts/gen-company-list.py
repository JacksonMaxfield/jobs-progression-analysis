import json
import requests
import codecs
import pandas as pd
import os
import time
import csv

# caller settings
callID = 0
configures = [
    {'pid' : "104323", 'pkey' : "ef8HfLzOp7A", 'pip' : "2601:602:8701:7a98:840c:8e86:a7c5:b332"},
    {'pid' : "108455", 'pkey' : "b3p135Es6Tc", 'pip' : "10.240.203.29"},
    {'pid' : "108481", 'pkey' : "fsAnlewSQho", 'pip' : "2601:602:8701:7a98:840c:8e86:a7c5:b332"},
    {'pid' : "108483", 'pkey' : "fv9G8dMEovs", 'pip' : "10.240.203.29"},
    {'pid' : "105144", 'pkey' : "8dfZEUklum", 'pip' : "2601:602:8701:7a98:840c:8e86:a7c5:b332"},
    {'pid' : "106918", 'pkey' : "C1GZIwosqE", 'pip' : "10.240.203.29"}
]

# glassdoor api call for finding locations of each company
def callAPILocations(ucompany):
    global callID
    global configures

    caller = configures[callID]
    url = "http://api.glassdoor.com/api/api.htm?useragent=Mozilla&format=json&v=1&action=jobs-stats"
    url += "&t.p=" + caller['pid']
    url += "&t.k=" + caller['pkey']
    url += "&userip=" + caller['pip']
    url += "&e=" + ucompany
    url += "&returnEmployers=" + "false"
    url += "&returnJobTitles=" + "true"
    url += "&jobType=" + "fulltime"
    url += "&returnCities=" + "true"
    url += "&useragent" + "Mozilla/5.0"

    hdr = {'User-Agent': 'Mozilla/5.0'}

    # actual request and response
    response = requests.get(url, headers=hdr)
    response.encoding = codecs.BOM_UTF8
    parsedJSON = response.json()

    if (callID < 5):
        callID = callID + 1
    else:
        callID = 0

    return(parsedJSON)

# takes in a list of strings and trims each element for commas, and suffixes such as Inc., Ltd., Corporation
def trimNames(namesList):
    trimmedNames = list()
    for element in namesList:
        string = element.strip(' ')
        string = string.replace(" Incorporated", "")
        string = string.replace(", Inc.", "")
        string = string.replace(", Inc", "")
        string = string.replace(" Inc.", "")
        string = string.replace(" Inc", "")
        string = string.replace(",Inc.", "")
        string = string.replace(",Inc", "")
        string = string.replace(" Corporation", "")
        string = string.replace(" Ltd.", "")

        string = string.replace("International Business Machines", "IBM")
        string = string.replace("Alphabet", "Google")
        string = string.replace("Taiwan Semiconductor Manufacturing Company", "TSMC")
        string = string.replace("Automatic Data Processing", "ADP")
        string = string.replace("NTT DOCOMO", "Docomo")
        string = string.replace("Broadcom Limited", "Broadcom")
        string = string.replace("Hewlett Packard Enterprise Company", "HP")
        string = string.replace("Cisco Systems", "Cisco")
        string = string.replace("Eaton, PLC", "Eaton")
        string = string.replace("Salesforce.com", "Salesforce")
        string = string.replace("Cognizant Technology Solutions", "Cognizant")
        string = string.replace("NXP Semiconductors N.V.", "NXP")
        string = string.replace("Infosys Limited", "Infosys")
        string = string.replace("SAP SE", "SAP")
        string = string.replace("Adobe Systems", "Adobe")
        string = string.replace("Yahoo!", "Yahoo")
        trimmedNames.append(string.strip(","))

    return trimmedNames

def printResultantCSV(listOfDict, fileName):
    keys = listOfDict[0].keys()
    keys = list(keys)

    with open(fileName, 'w', newline='') as output:
        writer = csv.DictWriter(output, fieldnames=keys)
        writer.writeheader()
        writer.writerows(listOfDict)

# creates a list of the top 30 technology companies, as ranked by NASDAQ
nasdaqList = pd.read_csv(os.path.join(os.path.dirname(__file__), "companylist.csv"))
nasdaqList = nasdaqList.sort_values(['MarketCap'], ascending=False)
nasdaqNameList = nasdaqList['Name'][:15].tolist()
nasdaqNameList = trimNames(nasdaqNameList)
nasdaqNameList = set(nasdaqNameList)


allLocationsList = []

for company in nasdaqNameList:
    locations = callAPILocations(company)
    returnedLocations = locations['response']['cities']
    time.sleep(0.18)

    for location in returnedLocations:
        toAppendDict = {}
        toAppendDict['company'] = company
        returnCity = str(location['name'])
        returnCity = returnCity.replace("&#039;", '')
        returnCity = returnCity[:-4]
        toAppendDict['city'] = returnCity
        toAppendDict['state'] = location['stateAbbreviation']

        allLocationsList.append(toAppendDict)


printResultantCSV(allLocationsList, 'all-company-locations.csv')
