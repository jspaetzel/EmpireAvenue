### This script automagically purchases one share in the 20 most recent users on EA. ###

import json
import urllib
import urllib2
from pprint import pprint

import connect

## Get shareholders, 
## Reinvestment priority: 

ticker = '' ## Optional, will default to connect.username otherwise

#### Random Setup Stuff ####
if ticker == '':
     ticker = connect.username
#### End Random Setup ######

#### Get Bank Balance ######
get = 'profile/bank/balance'
standardsend = '?apikey=' + connect.apikey + '&username=' + connect.username + '&password=' + connect.tkpw + '&ticker=' + ticker
response = urllib2.urlopen(connect.base_url + get + standardsend)
json_data = response.read()
###FILEALT###json_data = open('balance.htm',r,a)
parsed = json.loads(json_data) ## Loads the json into python as a dict
data = parsed['data'] ##Isolate the data portion of json
##pprint(data) ## TESTING
balance = data[0]['balance'] ## create balance variable
print(data[0]['balance']) #PrintBalance


#### Shareholders ####
start = '1'
page = 1
##data = []
collate = []
count = 0
while ( len(data) >= 99 or start == '1') : #### LOOP in order to get ENTIRE portfolio, multiple pages.. >< 
    get = 'portfolio/get'
    response = urllib2.urlopen(connect.base_url + get + standardsend + "&page=" + str(page))
    json_data = response.read()
    parsed = json.loads(json_data) ## Loads the json into python as a dict
    data = parsed['data'] ##Isolate the data portion of json
    #pprint(range(len(data)))
    #print(count)
    count = count + 1
    collate.extend(data)
    page = page + 1
    start = '0'
    
#print(range(len(collate)))
##pprint(collate)

meh = "List: "
meh2 = "List2: "
for i in range(len(collate)) :
    meh = meh + ', ' + collate[i]['ticker']
    meh2 = meh2 + ', ' + collate[i]['shares']
#print (meh)
#print (meh2)
for i in range(len(collate)) :
    #print(str(i) + " : " + str(collate[i]['ticker']) + " : " + str(collate[i]['shares'] ) )
    if int(collate[i]['shares']) <= 10:
        print ('ticker<10: ' + collate[i]['ticker'])
        shares_max = 0.70*float(collate[i]['your_shares_held']) ## I only want to buy up to 50% of how many they own of me
        if (shares_max > 200 ) :
            shares_max = 200 ## I am only capable of buying up to 200 shares currently...
        eves_max = float(balance)*0.40 ## Spend up to 40% of balance
        if shares_max > 0 :
            ## Get more information before buying
            get = 'profile/info'
            send = '?apikey=' + connect.apikey + '&username=' + connect.username + '&password=' + connect.tkpw + '&ticker=' + collate[i]['ticker']
            response = urllib2.urlopen(connect.base_url + get + send)
            json_data = response.read()
            parsed = json.loads(json_data) ## Loads the json into python as a dict
            profile = parsed['data'] ##Isolate the data portion of json
            pprint(profile)
            buypercent = 0.50 + ((abs((float(profile[0]['avg_div_per_share'])*100.0)-float(profile[0]['close']))/100.0)*5.0) ## 30% + if they have high divs increase by 5xthediff
            print('Buy Percent: ' + str(buypercent))
            
            #use the lower of these two numbers!
            want = float(shares_max)*float(buypercent) #Max that I want to buy
            afford = float(eves_max)/float(profile[0]['last_trade']) #Max that I can afford to buy
            
            buycount = want ## Hopefully I can get this many..
            
            if ( afford < want ) :
                buycount = afford ## I'll have to settle with how many I can afford
            if buycount > 300: ## My max is 300
                buycount = 300 - int(profile[0]['volume'])
            print('Attempt to purchase: ' + str(buycount) )
            buycountint = int(buycount)
            
            ## BUY Operation
            url = 'https://api.empireavenue.com/shares/buy'
            values = {
                      'apikey' : str(connect.apikey),
                      'username' : str(connect.username),
                      'password' : str(connect.tkpw),
                      'ticker' : str(profile[0]['ticker']),
                      'shares' : str(buycountint),
                      'last_trade' : str(profile[0]['last_trade']) 
                      }
    
            data2 = urllib.urlencode(values)
            req = urllib2.Request(url, data2)
            print(req)
            response = urllib2.urlopen(req)
            json_data = response.read()
            parsed = json.loads(json_data)
            pprint(parsed)
            ## END BUY OP
            ##505555555ut("Press ENTER to continue")

    else:
        print('aww no moar of you!')
                
### ROUND ONE
#### Do not already own any shares in that person...
#### Purchase max up to 50% of how many they own, spending max of 20%.
### ROUND TWO (NOT YET WRITTEN)
#### If I own shares but.. < 50% of how many other person owns...
#### Spend up to 20% of current balance on that person.
    
raw_input("Press ENTER to exit")
