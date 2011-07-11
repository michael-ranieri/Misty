#!/usr/bin/env python
# Copyright (C) 2011 Michael Ranieri <michael.d.ranieri at gmail.com>

import sys, json, re, shelve

def main(params):
    msg, user, channel, users = params
    
    receiver, msg = re.split(':', msg, 1)
    
    for k, u in users.iteritems():
        if receiver == k and u == 'H':
            sys.exit(0)
            
    db = shelve.open('tShelve')
    try:
        temp = db[receiver]
    except:
        temp = []
        
    temp.append({
        'sender' : user,
        'msg' : msg
    })
    
    db[receiver] = temp
    db.close()
    
    print "Don't worry %s! I will make sure to give %s that message." % (user, receiver)

if __name__ == '__main__':
    params = json.loads(sys.argv[1])
    main(params)
    