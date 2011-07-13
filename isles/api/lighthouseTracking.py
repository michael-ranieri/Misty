#!/usr/bin/env python
# Copyright (C) 2011 Michael Ranieri <michael.d.ranieri at gmail.com>

# System imports
import urllib2
import json
import sys
import re
from xml.dom import minidom

# Misty imports
import settings_local as settings


def main(params):
    
    msg, user, channel, users = params
    
    searchTerms = re.split(' ', msg)
    
    tickets = []

    for url in settings.LIGHTHOUSE_PROJECT_URL:
        
        req = urllib2.Request(url + '/tickets.xml?limit=100&q=not-state:closed')
        req.add_header("X-LighthouseToken", settings.LIGHTHOUSE_KEY)
        req.add_header("Content-Type", 'application/xml')
        
        response = minidom.parseString(urllib2.urlopen(req).read())

        temp = response.getElementsByTagName('tickets')[0].getElementsByTagName('ticket')
        
        

        for i in temp:
            tickets.append({
                'title' : i.getElementsByTagName('title')[0].firstChild.data,
                'age'   : i.getElementsByTagName('updated-at')[0].firstChild.data,
                'score' : 0,
                'url'   : url + '/tickets/' + i.getElementsByTagName('number')[0].firstChild.data \
                                + '-' + i.getElementsByTagName('permalink')[0].firstChild.data
            })
    
    for t in tickets:
        for term in searchTerms:
            if re.search(term, t['title'], re.IGNORECASE):
                t['score'] += 1
                
    def sortScore(ticket):
        return ticket['score']
    def sortAge(ticket):
        return ticket['age']

    tickets.sort(key=sortAge, reverse=True)
    tickets.sort(key=sortScore,reverse=True)
    
    if len(tickets) > 0 and tickets[0]['score'] > 0:
        print tickets[0]['url']
            
            
if __name__ == '__main__':
    params = json.loads(sys.argv[1])
    main(params)