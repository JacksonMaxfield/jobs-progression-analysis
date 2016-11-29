import json
import requests
import codecs
import pandas as pd
import os
import csv
import operator
import time
import sys
from difflib import SequenceMatcher

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

# general glassdoor API call function
def callAPIJobs(ucompany, ucity, ustate,):
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
    url += "&city=" + ucity
    url += "&state=" + ustate
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

# glassdoor api call for jobs-prog for single job
def callAPIProg(ujob):
    global callID
    global configures

    caller = configures[callID]
    url = "http://api.glassdoor.com/api/api.htm?useragent=Mozilla&format=json&v=1&action=jobs-prog"
    url += "&t.p=" + caller['pid']
    url += "&t.k=" + caller['pkey']
    url += "&userip=" + caller['pip']
    url += "&countryId=" + "1"
    url += "&jobTitle=" + ujob
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

# glassdoor api call for finding locations of each company
def callAPICompany(ucompany):
    global callID
    global configures

    caller = configures[callID]
    url = "http://api.glassdoor.com/api/api.htm?useragent=Mozilla&format=json&v=1&action=employers"
    url += "&t.p=" + caller['pid']
    url += "&t.k=" + caller['pkey']
    url += "&userip=" + caller['pip']
    url += "&q=" + ucompany
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

def printDict(d, indent=0):
   for key, value in iter(d.items()):
      print ('\t' * indent + str(key))
      if isinstance(value, dict):
         printDict(value, indent+1)
      else:
         print ('\t' * (indent+1) + str(value))

def similar(a, b):
    return SequenceMatcher(None, a, b).ratio()

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
nasdaqNameList = nasdaqList['Name'][6:7].tolist() #REPLACE
nasdaqNameList = trimNames(nasdaqNameList)
nasdaqNameList = set(nasdaqNameList)
nasdaqNameList = list(nasdaqNameList)

allLocationsList = []

for company in nasdaqNameList:
    locations = callAPILocations(company)
    if 'response' not in locations:
        printResultantCSV(allLocationsList, 'incomplete-location-call.csv')
        print('broke in locations call')
        print('file returned: all locations list')
        sys.exit()

    time.sleep(0.22)
    returnedLocations = locations['response']['cities']
    companyInfo = callAPICompany(company)
    if 'response' not in companyInfo:
        printResultantCSV(allLocationsList, 'incomplete-location-call.csv')
        print('broke in company info call')
        print('file returned: all locations list')
        sys.exit()

    time.sleep(0.22)
    companyStats = companyInfo['response']['employers'][0]
    CaVRating = companyStats['cultureAndValuesRating']
    SLRating = companyStats['seniorLeadershipRating']
    CaBRating = companyStats['compensationAndBenefitsRating']
    CORating = companyStats['careerOpportunitiesRating']
    WLBRating = companyStats['workLifeBalanceRating']

    for location in returnedLocations:
        toAppendDict = {}
        toAppendDict['company'] = company
        returnCity = str(location['name'])
        returnCity = returnCity.replace("&#039;", '')
        returnCity = returnCity[:-4]
        toAppendDict['city'] = returnCity
        toAppendDict['state'] = location['stateAbbreviation']
        toAppendDict['CaVRating'] = CaVRating
        toAppendDict['SLRating'] = SLRating
        toAppendDict['CaBRating'] = CaBRating
        toAppendDict['CORating'] = CORating
        toAppendDict['WLBRating'] = WLBRating

        allLocationsList.append(toAppendDict)

del nasdaqList
del nasdaqNameList

allJobsList = []

for location in allLocationsList:
    jobs = callAPIJobs(location['company'], location['city'], location['state'])
    if 'response' not in jobs:
        printResultantCSV(allJobsList, 'incomplete-jobs-call.csv')
        print('broke in company jobs by location call')
        print('file returned: all jobs list')
        sys.exit()

    time.sleep(0.22)
    returnedJobs = jobs['response']['jobTitles']

    for job in returnedJobs:
        toAppendDict = {}
        toAppendDict['company'] = location['company']
        toAppendDict['city'] = location['city']
        toAppendDict['state'] = location['state']
        toAppendDict['jobId'] = job['id']
        toAppendDict['title'] = job['jobTitle']
        toAppendDict['numJobs'] = job['numJobs']
        toAppendDict['CaVRating'] = location['CaVRating']
        toAppendDict['SLRating'] = location['SLRating']
        toAppendDict['CaBRating'] = location['CaBRating']
        toAppendDict['CORating'] = location['CORating']
        toAppendDict['WLBRating'] = location['WLBRating']

        allJobsList.append(toAppendDict)

del allLocationsList

finalJobsList = []
jobIndex = 0
for job in allJobsList:
    containsSeniority = True
    if (('Chief' not in job['title']) and
    ('Director' not in job['title']) and
    ('Manager' not in job['title']) and
    ('President' not in job['title']) and
    ('Partner' not in job['title']) and
    ('Senior' not in job['title']) and
    ('Principal' not in job['title']) and
    ('Sr.' not in job['title']) and
    ('Lead' not in job['title']) and
    ('VP' not in job['title']) and
    ('Executive' not in job['title']) and
    ('2' not in job['title']) and
    ('II' not in job['title']) and
    ('Vice President' not in job['title'])):
        containsSeniority = False

    if not containsSeniority:
        progression = callAPIProg(job['title'])
        if 'response' not in progression:
            printResultantCSV(finalJobsList, 'incomplete-prog-call.csv')
            print('broke in job progression call')
            print('file returned: final jobs list')
            sys.exit()

        time.sleep(0.22)
        returnedProg = progression['response']['results']
        returnedProg.sort(key=operator.itemgetter('medianSalary'))

        indexOfMostSimilar = 0
        highestSimilar = 0
        index = 0
        for progJob in returnedProg:
            computedSimilar = similar(job['title'], progJob['nextJobTitle'])
            if computedSimilar > highestSimilar:
                highestSimilar = computedSimilar
                indexOfMostSimilar = index

            progJob['similarity'] = computedSimilar
            index = index + 1

        if (indexOfMostSimilar + 2) < len(returnedProg):
            job['nextJobOne'] = returnedProg[indexOfMostSimilar + 1]['nextJobTitle']
            job['nextJobTwo'] = returnedProg[indexOfMostSimilar + 2]['nextJobTitle']
        elif (indexOfMostSimilar + 1) < len(returnedProg):
            job['nextJobOne'] = returnedProg[indexOfMostSimilar + 1]['nextJobTitle']
            job['nextJobTwo'] = ''
        else:
            job['nextJobOne'] = ''
            job['nextJobTwo'] = ''

        job['id'] = jobIndex
        finalJobsList.append(job)
        jobIndex = jobIndex + 1


printResultantCSV(finalJobsList, 'completed-full-data-oracle.csv')
