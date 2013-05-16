### This script automagically purchases one share in the 20 most recent users on EA. ###

import json
import urllib
import urllib2
from pprint import pprint

import connect
base = connect.base_url
key = connect.key

#### Random Setup Stuff ####
if ticker == '':
     ticker = username
#### End Random Setup ######

#### Get Bank Balance ######
get = 'profile/bank/balance'
send = '&ticker=' + ticker
response = urllib2.urlopen(base + get + key + endsend)
json_data = response.read()
###FILEALT###json_data = open('balance.htm',r,a)
parsed = json.loads(json_data) ## Loads the json into python as a dict
data = parsed['data'] ##Isolate the data portion of json
##pprint(data) ## TESTING
balance = data[0]['balance'] ## create balance variable
print(data[0]['balance']) #PrintBalance


#### Recent ####
get = 'leaders/recent/people'
response = urllib2.urlopen(base_url + get + send)
json_data = response.read()
parsed = json.loads(json_data) ## Loads the json into python as a dict
recent = parsed['data'] ##Isolate the data portion of json

#### Assemble ticker array from recent data ####
tickers = []
for i in range(len(recent)) :
    tickers.append(recent[i]['ticker'])
    
##pprint(tickers)

#### Generate request ####
send = '&ticker=' 
for i in range(len(tickers)):
    if ( i == 0 ) :
        send = send + tickers[i]
    else :
        send = send + ',' + tickers[i]
##print(send)

get = 'profile/info'
response = urllib2.urlopen(base + get + send)
json_data = response.read()
parsed = json.loads(json_data) ## Loads the json into python as a dict
#print(parsed)
data = parsed['data'] ##Isolate the data portion of json

for i in range(len(data)):
    #if ( int(data[i]['held_shares']) == 0 ) :
        print (str(data[i]['ticker']) + ' ' + str(data[i]['held_shares']))
        
        url = 'shares/buy'
        values = {
                  'apikey' : str(connect.apikey),
                  'username' : str(connect.username),
                  'password' : str(connect.tkpw),
                  'ticker' : str(data[i]['ticker']),
                  'shares' : str(200),
                  'last_trade' : str(data[i]['last_trade']) 
                  }

        data2 = urllib.urlencode(values)
        req = urllib2.Request(base+url, data2)
        print(req)
        response = urllib2.urlopen(req)
        json_data = response.read()
        parsed = json.loads(json_data)
