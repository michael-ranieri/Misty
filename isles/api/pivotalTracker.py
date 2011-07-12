#!/usr/bin/env python
# Copyright (C) 2011 Michael Ranieri <michael.d.ranieri at gmail.com>

# System imports
import sys, json, urllib2, re, string
from xml.dom import minidom

# Misty imports
import settings_local as settings

def main(params):
    msg, user, channel, users = params
    
    searchTerms = re.split(' ', msg)
    
    API_URL = ('http://www.pivotaltracker.com/services/v3/projects/'
                      + settings.PIVOTAL_PROJECT
                      + '/iterations/current')

    req = urllib2.Request(API_URL,
                          None,
                          {'X-TrackerToken': settings.PIVOTAL_KEY})
    response = minidom.parseString(urllib2.urlopen(req).read())

    iterations = response.getElementsByTagName('iterations')[0].getElementsByTagName('iteration')

    stories = []

    for i in iterations:

        temp = i.getElementsByTagName('stories')[0].getElementsByTagName('story')

        for s in temp:
            stories.append({
                'name'              : string.lower(s.getElementsByTagName('name')[0].firstChild.data),
                'url'               : string.lower(s.getElementsByTagName('url')[0].firstChild.data),
                'score'             : 0,
                'iteration'         : i.getElementsByTagName('number')[0].firstChild.data
            })

    for s in stories:
        for term in searchTerms:
            if re.search('%s' % term, s['name']):
                s['score'] += 1

    def sortScore(story):
        return story['score']
    def sortStatus(story):
        return story['iteration']
        
    stories.sort(key=sortStatus, reverse=True)
    stories.sort(key=sortScore, reverse=True)

    if len(stories) > 0 and stories[0] > 0:
        print stories[0]['url']
        
if __name__ == '__main__':
    params = json.loads(sys.argv[1])
    main(params)