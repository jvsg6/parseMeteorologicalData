#!/usr/bin/python2.7
# -*- coding: utf-8 -*-
import sys
import os
import bs4
import requests
import time

citeName = "https://www.gismeteo.ru/diary/"
headers = { 'User-Agent': 'Mozilla/5.0 (Windows NT 6.0; WOW64; rv:24.0) Gecko/20100101 Firefox/24.0' }


def main():
    cityId = "227639/"
    year = "2018"
    
    for mnthId in range(1,13):
        linkToRegion = citeName+cityId+year+"/{0}/".format(mnthId)
        print linkToRegion
        s = requests.get(linkToRegion, headers=headers)
        pageData=bs4.BeautifulSoup(s.text, "html.parser")
	table = pageData.find("table")
        linesInTable = table.find_all('tr')
	linesInTable = linesInTable[2:]
	linkData = linesInTable[0].find_all('td')[2].getText()
	print linkData
    print "Dine!"
    return
    
if __name__ == "__main__":
    sys.exit(main())