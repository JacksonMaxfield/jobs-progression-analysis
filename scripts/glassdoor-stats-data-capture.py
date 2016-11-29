# -*- coding: utf-8 -*-
import json
import requests
import codecs

# caller settings
jconfigure = {'pid' : "104323", 'pkey' : "ef8HfLzOp7A", 'pip' : "2601:602:8701:7a98:95ad:e495:5650:8c4e"}

def callAPI(caller, ucompany, uquery, ucity, ustate, ucountry):
    url = "http://api.glassdoor.com/api/api.htm?useragent=Mozilla&format=json&v=1&action=jobs-stats"
    url += "&t.p=" + caller['pid']
    url += "&t.k=" + caller['pkey']
    url += "&userip=" + caller['pip']
    url += "&e=" + ucompany
    url += "&returnEmployers=" + "false"
    url += "&returnJobTitles=" + "true"
    url += "&jobType=" + "fulltime"
    url += "&q=" + uquery
    url += "&city=" + ucity
    url += "&state=" + ustate
    url += "&country=" + ucountry
    url += "&useragent" + "Mozilla/5.0"

    hdr = {'User-Agent': 'Mozilla/5.0'}

    # actual request and response
    response = requests.get(url, headers=hdr)
    response.encoding = codecs.BOM_UTF8
    parsedJSON = response.json()
    return(parsedJSON)

# call and store
tcompany = 'Google'
tcity = ''
tquery = ''

returnedData = callAPI(jconfigure, tcompany, tquery, tcity, '', '')
outputFile = tcompany + '-' + tcity + '-jobs-data'

# outputs call to JSON file
file = open(outputFile + ".json", "w")
json.dump(returnedData, file, indent=4, separators=(',', ': '))
file.close()
