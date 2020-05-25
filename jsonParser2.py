import json
import urllib.request
import sqlite3

#pull latest data into file
def pullData():
    data = urllib.request.urlopen("https://frontlinehelp.api.ushahidi.io/api/v3/posts/geojson").read()
    serialData = json.loads(data)
    with open('data.json','w',encoding='utf-8') as file:
        json.dump(serialData,file)

#read data from file
def readGeoData():
    with open('data.json','r') as file:
        data = file.read()
    return json.loads(data)

"""
read record data from file
depracated since no longer needed
"""
#def readRecordData():
#    with open('record.json','r') as file:
#        data = file.read()
#    return json.loads(data)

#find number of records
def findRange(data):
    try:
        x = 0
        while True:
            data['features'][x]
            x+=1
    except IndexError: #catch index out of bounds, indicates latest element
        return x-1

#returns lat,long for a specified id
def findCoords(geoData,recordID):
    coords = geoData['features'][recordID]['geometry']['geometries'][0]['coordinates']
    longitude = coords[0]
    latitude = coords[1]
    return latitude,longitude

#grab url links
def findURL(data,recordID):
    return data['features'][recordID]['properties']['url']

"""
follow url and dump data
same method as pullData
depracated since inefficient read/writing
"""
#def followUrlDumpData(url):
#    data = urllib.request.urlopen(url).read()
#    serialData = json.loads(data) #serialise data
#    with open('record.json','w',encoding='utf-8') as file:
#        json.dump(serialData,file)

#get specific record url (in memory)
def followUrlRetData(url):
    data = urllib.request.urlopen(url).read()
    return json.loads(data) #serialise data

#insert to database
def insertToDB(recordID,formID,lat,long,postcode,url):
    c.execute('INSERT INTO records VALUES(?,?,?,?,?,?)',(recordID,formID,lat,long,postcode,url))
    conn.commit()

#get record id
def findID(recordData):
    return recordData['id']

#get form id
def findFormID(recordData):
    return recordData['form']['id']

"""
try find postcode based on key (hash)
if key doesnt work return null
"""
def findPostcode(recordData):
    try:
        return recordData['values']['ecd7d7fd-da36-4ace-a78a-571c5e296ad4'][0]
    except:
        return None

#dump all info into db
def dumpRecordsToDB(geoData,recordRange):
    for i in range(0,recordRange):
        try:
            recordData = followUrlRetData(findURL(geoData,i))
            recordID = findID(recordData)
            formID = findFormID(recordData)
            latitude,longitude = findCoords(geoData,i)
            postcode = findPostcode(recordData)
            insertToDB(recordID,formID,latitude,longitude,postcode,findURL(geoData,i))
        except KeyError as e:
            print(e)
            continue

def geoJson():
    pullData()
    geoData = readGeoData()
    recordRange = findRange(readGeoData())
    dumpRecordsToDB(geoData,recordRange)

    conn.close() #disconnect from db
conn = sqlite3.connect('insights.db') #connect to db
c = conn.cursor() #create cursor obj
geoJson()
