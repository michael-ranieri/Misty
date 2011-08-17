#!/usr/bin/env python
# Copyright (C) 2011 Michael Ranieri <michael.d.ranieri at gmail.com>

import sys
import json
import re
import shelve


def main(params):
    msg, user, channel, users = params
    
    user = user.encode('utf-8')
    db = shelve.open('tShelve')

    for rec in db:
        for message in db[rec]:
            if message['sender'] == user:
                print "Sending '%s' to %s" % (message['msg'], rec)
    
    db.close()
if __name__ == '__main__':
    params = json.loads(sys.argv[1])
    main(params)