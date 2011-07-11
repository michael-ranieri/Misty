#!/usr/bin/env python
# Copyright (C) 2011 Michael Ranieri <michael.d.ranieri at gmail.com>

import time, sys, json
params = json.loads(sys.argv[1])
msg, user, channel, users = params

print user + " sent a message to channel " + channel

time.sleep(10)

print "Here is the message that was sent 10 seconds ago:"
print msg