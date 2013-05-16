### This script automagically purchases one share in the 20 most recent users on EA. ###

import json
import urllib
import urllib2
from pprint import pprint

import connect

ticker = '' ## Optional, will default to connect.username otherwise
bank = False

#### Random Setup Stuff ####
if ticker == '':
     ticker = connect.username
#### End Random Setup ######

## Create the basic send statement
send = '?connect.apikey=' + connect.apikey + '&connect.username=' + connect.username + '&password=' + connect.tkpw

#### Get Bank Balance ######
if bank == True :
	get = 'profile/bank/balance'
	response = urllib2.urlopen(connect.base_url + get + send)
	json_data = response.read()
	###FILEALT###json_data = open('balance.htm',r,a)
	parsed = json.loads(json_data) ## Loads the json into python as a dict
	data = parsed['data'] ##Isolate the data portion of json
	##pprint(data) ## TESTING
	balance = data[0]['balance'] ## create balance variable
	print("Current Balance" + data[0]['balance']) #PrintBalance


#### Recent ####
#get = 'leaders/change'
#response = urllib2.urlopen(connect.base_url + get + standardsend)
#json_data = response.read()
#parsed = json.loads(json_data) ## Loads the json into python as a dict
#recent = parsed['data'] ##Isolate the data portion of json

get = 'leaders/change'##ALTER LINE TO CHANGE WHAT LIST IM BUYING FROM
response = urllib2.urlopen(connect.base_url + get + send)
json_data = response.read()
parsed = json.loads(json_data) ## Loads the json into python as a dict
data = parsed['data'] ##Isolate the data portion of json

#gen profile request, make a string of the tickers in groups of 20
tickers = [','.join(item['ticker'] for item in data[idx:idx+20]) for idx in xrange(0,len(data),20)]

print(tickers[0])
print(tickers[1])


for i in data:
    for v in tickers :
        get = 'profile/info' 
        response = urllib2.urlopen(connect.base_url + get + send + '&ticker=' + v)
        print ( connect.base_url + get + send + '&ticker=' + v) #debug		
        json_data = response.read()
        parsed = json.loads(json_data)
        profile = parsed['data']   
        
        meh = ""
        for m, p in enumerate(profile) :        
            #print("Held Shares" + " " + str(p['held_shares']) + " " + str(p['ticker']))
            #raw_input("Press ENTER to continue")
        
            #Procede if I dont already own any
            if p['held_shares'] == 0  : 
                #print("Held Shares: " + str(p['held_shares']) + " of " + str(p['ticker']))
                
                # If they have decent divs we should buy them...
                if ( float(p['avg_div_per_share'])/float(p['last_trade']) < 1.2 ) :
        
                    url = 'https://api.empireavenue.com/shares/buy'
                    values = {
                              'connect.apikey' : str(connect.apikey),
                              'connect.username' : str(connect.username),
                              'password' : str(connect.tkpw),
                              'ticker' : str(p['ticker']),
                              'shares' : str(1),
                              'last_trade' : str(p['last_trade']) 
                              }
                    bought = urllib.urlencode(values)
                    req = urllib2.Request(url, bought)
                    
                    response = urllib2.urlopen(req)
                    json_data = response.read()
                    parsed = json.loads(json_data)
                    bought = parsed['data']
                    print("Ticker: " + str(p['ticker']) + ". Owned: " + str(bought[0]['shares_owned']) + ". Charged: " + str(bought[0]['total_charged']) + ".")
    
