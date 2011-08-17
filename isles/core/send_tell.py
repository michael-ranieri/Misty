#!/usr/bin/env python
# Copyright (C) 2011 Michael Ranieri <michael.d.ranieri at gmail.com>

import sys
import json
import re
import shelve


def main(params):
    msg, user, channel, users = params

    user = user.encode('utf-8').lower()
    
    db = shelve.open('tShelve')
    try:
        temp, db[user] = db[user], []
        db.close()
    except:
        sys.exit(0)

    if temp != []:
        print "Hey %s! You have %s messages." % (user, len(temp))
        for t in temp:
            print '%s said "%s"' % (t['sender'], t['msg'])


if __name__ == '__main__':
    params = json.loads(sys.argv[1])
    main(params)