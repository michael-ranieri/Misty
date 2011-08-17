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

    if re.search('--clear', msg) or re.search('-c', msg):
        for rec in db:
            temp = db[rec]
            to_delete = []
            for message in temp:
                if message['sender'] == user:
                    print "Deleting '%s' to %s" % (message['msg'], rec)
                    to_delete.append(message)

            for i in to_delete: temp.remove(i)
            db[rec] = temp
    else:
        for rec in db:
            for message in db[rec]:
                if message['sender'] == user:
                    print "Sending '%s' to %s" % (message['msg'], rec)

    db.close()
if __name__ == '__main__':
    params = json.loads(sys.argv[1])
    main(params)