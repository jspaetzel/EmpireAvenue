#!/usr/bin/python
# -*- coding: utf-8 -*-
import json
import urllib
import urllib2
from pprint import pprint
import connect

#### Collect all Shareholders ####
start = '1'
page = 1
collate = []
mcollate =[]
count = 0 # for tracking requests
data = ''
while ( len(data) >= 99 or start == '1') : #### LOOP in order to get ENTIRE portfolio, multiple pages.. >< 
    get = 'portfolio/get'
    response = urllib2.urlopen(connect.base_url + get + connect.key + "&page=" + str(page))
    json_data = response.read()
    parsed = json.loads(json_data) ## Loads the json into python as a dict
    meta = parsed['meta']
    if meta['requests'] < 150:
        print meta['requests']
        data = parsed['data'] ##Isolate the data portion of json
        collate.extend(data)
        count = count + 1
        page = page + 1
        start = '0'
    else:
        print "All requests used"
        break

#### Time to create a list of things to buy ####
for i in range(len(collate)) :
    #if int(mcollate[i]['requests']) == 150:
    #    break
    values=None
    if float(collate[i]['yesterday_highest']) < 23:
        # We no longer want to own anyone with shareprice < 23
        url = 'https://api.empireavenue.com/shares/sell'
        values = {
                    'apikey' : str(connect.apikey),
                    'username' : str(connect.username),
                    'password' : str(connect.tkpw),
                    'ticker' : str(collate[i]['ticker']),
                    'shares' : str(collate[i]['shares']),
                    'last_trade' : str(collate[i]['last_trade'])
                    }
    elif int(collate[i]['shares']) < 600: # I can still buy shares in this account.
        ## i dont own 300 yet.. so lets buy one
        url = 'https://api.empireavenue.com/shares/buy'
        values = {
                    'apikey' : str(connect.apikey),
                    'username' : str(connect.username),
                    'password' : str(connect.tkpw),
                    'ticker' : str(collate[i]['ticker']),
                    'shares' : str(1),
                    'last_trade' : str(collate[i]['last_trade'])
                    }
    if (values):
        data2 = urllib.urlencode(values)
        req = urllib2.Request(url, data2)
        response = urllib2.urlopen(req)
        json_data = response.read()
        parsed = json.loads(json_data)
        if parsed['meta']['requests'] == 150:
            break
        if parsed['data'][0]['bank_balance'] < 100:
            break
        print(collate[i]['ticker'])

