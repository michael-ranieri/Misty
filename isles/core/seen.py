#!/usr/bin/env python
# Copyright (C) 2011 Michael Ranieri <michael.d.ranieri at gmail.com>

import sys
import json
import re
import datetime
import time


def main(params):
    msg, user, channel, users = params
    
    target = re.split(' ', msg, 1)[1]
    
    for k, u in users.iteritems():
        if k == target and re.search('G', u['status']):
            delta = datetime.timedelta(seconds = int(time.time()) - u['last_seen'])
            print "%s was last seen %s ago. [hrs : min : sec]" % (target, delta)

    

if __name__ == '__main__':
    params = json.loads(sys.argv[1])
    main(params)