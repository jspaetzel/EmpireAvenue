### This script returns number of free api requests.

import json
import urllib
import urllib2
from pprint import pprint

import connect
base = connect.base_url
get = 'profile/bank/balance'
key = connect.key

response = urllib2.urlopen(base + get + key)
json_data = response.read()
parsed = json.loads(json_data) ## Loads the json into python as a dict
meta = parsed['meta'] ##Isolate the data portion of json
if ( meta['requests']  == 150 ) :
    print('Request limit reached.')
else :
    print(str(150 - meta['requests']) + ' requests remaining')

