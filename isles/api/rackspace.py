#!/usr/bin/env python
# Copyright (C) 2011 Michael Ranieri <michael.d.ranieri at gmail.com>

# System imports
import urllib2
import json
import sys
import re

# Misty imports
import settings_local as settings


def printMatch(server):
    print "Rackspace server %s has the Public IP(s):" % server['name']
    for ip in server['public']:
        print ip
    print "and Private IP(s):"
    for ip in server['private']:
        print ip

def main(params):
    msg, user, channel, users = params
    
    searchTerms = re.split(' ', msg)
    
    req = urllib2.Request('https://auth.api.rackspacecloud.com/v1.0')
    req.add_header("X-Auth-User", settings.RACKSPACE_USER)
    req.add_header("X-Auth-Key", settings.RACKSPACE_KEY)
    
    response = urllib2.urlopen(req)
    
    RACKSPACE_TOKEN = response.headers['x-auth-token']
    RACKSPACE_URL = response.headers['X-Server-Management-Url']
    
    req = urllib2.Request(RACKSPACE_URL + '/servers/detail')
    req.add_header("Content-Type", 'application/json')
    req.add_header("Accept", 'application/json')
    req.add_header("X-Auth-Token", RACKSPACE_TOKEN)
    
    response = json.loads(urllib2.urlopen(req).read())
    
    servers = []

    for server in response['servers']:
        servers.append({
            'id' : server['id'],
            'name' : server['name'],
            'public' : server['addresses']['public'],
            'private' : server['addresses']['private']
        })
    
    for server in servers:
        for term in searchTerms:
            if term == server['id'] \
            or term == server['name']:
                printMatch(server)
                
            for ip in server['public']:
                if term == ip:
                    printMatch(server)
            
            for ip in server['private']:
                if term == ip:
                    printMatch(server)
                    

if __name__ == '__main__':
    params = json.loads(sys.argv[1])
    main(params)