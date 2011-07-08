#!/usr/bin/env python
# Copyright (C) 2011 Michael Ranieri <michael.d.ranieri at gmail.com>

import time, sys

print sys.argv[2] + " sent a message to channel " + sys.argv[3]

time.sleep(10)

print "Here is the message that was sent 10 seconds ago:"
print sys.argv[1]