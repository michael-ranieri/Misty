import urllib2
import json


TESTDATA = {'username': 'user',
            'password': 'password',
            'messages': ['this is a message',
                       'posted over json',
                       ]}
URL = 'http://localhost:8880/'

jsondata = json.dumps(TESTDATA)
print jsondata

req = urllib2.Request(url = URL,
                      data = jsondata)

r = urllib2.urlopen(req)

print r.read()