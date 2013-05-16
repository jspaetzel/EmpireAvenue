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
response = urllib2.urlopen(base + get + key)

json_data = response.read()
###FILEALT###json_data = open('balance.htm',r,a)
parsed = json.loads(json_data) ## Loads the json into python as a dict
data = parsed['data'] ##Isolate the data portion of json
##pprint(data) ## TESTING
balance = data[0]['balance'] ## create balance variable
print(data[0]['balance']) #PrintBalance

#### Get full portfolio ####
get = 'portfolio/get'
response = urllib2.urlopen(base_url + get + standardsend)
json_data = response.read()
parsed = json.loads(json_data) ## Loads the json into python as a dict
data = parsed['data'] ##Isolate the data portion of json
##pprint(data)
porfolio_count = len(data) ## determines size of portfolio
data.pop(porfolio_count-1) ## Pops out the last integers.. To be modified for use in loop.
##pprint(data)
count = 0
for i in range(len(data)):
    lowest = float(data[i]['yesterday_lowest'])
    close = float(data[i]['close'])
    diff = close-lowest
    print(data[i]['yesterday_lowest'] + " " + data[i]['close'] + " " + data[i]['ticker'] ) ## HOW ACTIVE ARE THEY?
    
    ##print(diff)
    if ( lowest ) > ( close ) : ## Detects a reduction in price
        ##get = 'profile/info'
        print(str(diff) + data[i]['ticker'])
        if diff > float(0.5) :
            print(data[i]['ticker'])
            print('yesterday\'s low: ' + str(lowest))
            print('close: ' + str(close) )
            print('diff: ' + str(diff))
            print('\n')
            count = count + 1

print('Count: ' + str(count))
print('Total: ' + str(porfolio_count))
        
