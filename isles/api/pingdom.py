#!/usr/bin/env python
# Copyright (C) 2011 Michael Ranieri <michael.d.ranieri at gmail.com>

# System imports
import urllib2
import json
import base64

# Misty imports
import settings_local as settings


def allChecks(iterable):
    for i in iterable:
        if i['status'] != 'up':
            return False
    return True

def main():
    
    pingBaseURL = 'https://api.pingdom.com'
    
    AUTH = base64.b64encode(settings.PINGDOM_USER + ':' + settings.PINGDOM_PASSWORD)

    req = urllib2.Request(pingBaseURL + '/api/2.0/checks')
    req.add_header("App-Key", settings.PINGDOM_KEY)
    req.add_header("Authorization", 'Basic ' + AUTH)
    
    response = urllib2.urlopen(req)

    msg = json.loads(response.read())

    checks = []

    for check in msg['checks']:
        checks.append({
            'name' : check['name'],
            'status' : check['status']
        })
        

    if allChecks(checks):
        print "Pingdom reports that all %s checks are good!" % len(checks)
        sys.exit(0)
    else:
        for check in checks:
            if check['status'] == 'down':
                print check['name'] + ' || ' + check['status']
                

if __name__ == '__main__':
    main()