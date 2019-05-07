#!/usr/bin/python2.7
# -*- coding: utf-8 -*-
import sys
import os
import bs4
import requests
import time

citeName = "https://www.gismeteo.ru/diary/"
headers = { 'User-Agent': 'Mozilla/5.0 (Windows NT 6.0; WOW64; rv:24.0) Gecko/20100101 Firefox/24.0' }

first = True


def parseTemp(lineData, shift):
    return int(lineData[1+shift].getText())
    
def parsePressure(lineData, shift):
    return int(lineData[2+shift].getText())

def parseCloud(lineData, shift):
    cloud = lineData[3+shift].find("img").get("src").split("/")[-1].split(".")[0]
    if(cloud == "sun"):
        cloud = 1
    if(cloud == "sunc"):
        cloud = 3
    if(cloud == "suncl"):
        cloud = 5
    if(cloud == "dull"):
        cloud = 10
    return cloud
    
    
def parseWeather(lineData, shift):
    weather = None
    try:
        weather = lineData[4+shift].find("img").get("src").split("/")[-1].split(".")[0]
	if weather == "snow":
	    weather = 2
	if weather == "rain":
	    weather = 1
	if weather == "storm":
	    weather = 1
    except AttributeError:
        weather = 0
    return weather
    
def parseWindData(lineData, shift):
    windData = lineData[5+shift].find("span").getText()
    windSpeed = int(windData.split(" ")[-1].split(u"м")[0])
    windDir = windData.split(" ")[0]
    
    if(windDir == u"С"):
        windDir = 0
    if(windDir == u"СВ"):
        windDir = 45
    if(windDir == u"В"):
        windDir = 90
    if(windDir == u"ЮВ"):
        windDir = 135
    if(windDir == u"Ю"):
        windDir = 180
    if(windDir == u"ЮЗ"):
        windDir = 225
    if(windDir == u"З"):
        windDir = 270
    if(windDir == u"СЗ"):
        windDir = 315
    return windSpeed, windDir
    
def parseLine(lineData, shift):

    temp = parseTemp(lineData, shift)
    pr = parsePressure(lineData, shift)
    cloud = parseCloud(lineData, shift)
    weather = parseWeather(lineData, shift)
    windSpeed, windDir = parseWindData(lineData, shift)
    
    return {"temp": temp, "pressure": pr, "cloud": cloud, "weather": weather, "windSpeed": windSpeed, "windDir": windDir}

def parseTable(pageData):
    table = pageData.find("table")
    linesInTable = table.find_all('tr')
    linesInTable = linesInTable[2:]
    for fullLine in linesInTable:
        try:
            day = parseLine(fullLine.find_all('td'), 0)
            night = parseLine(fullLine.find_all('td'), 5)
	except ValueError:
	    print "No Data in line"
	except AttributeError:
	    print "No Data in line"
    return

def main():
    cityId = "227639/"
    year = "2018"
    
    for mnthId in range(1,13):
        linkToRegion = citeName+cityId+year+"/{0}/".format(mnthId)
        print linkToRegion
        s = requests.get(linkToRegion, headers=headers)
        pageData=bs4.BeautifulSoup(s.text, "html.parser")
	parseTable(pageData)

	
    print "Dine!"
    return
    
if __name__ == "__main__":
    sys.exit(main())