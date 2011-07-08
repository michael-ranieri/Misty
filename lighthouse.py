#!/usr/bin/env python
# Copyright (C) 2011 Michael Ranieri <michael.d.ranieri at gmail.com>

# input to methods will be a tuple (Message from irc, user who sent msg, channel)
# Must return a tuple (bool, string, string)
# bool is whether or not you want to send this particular message to your Isle for processing
# The first string is the relative location of the isle from the settings.PATH_TO_ISLE
# The second string is the filename of the isle.

# NOTE: some messages beginning with {nickname}: are reserved for internal functions
# Try to avoid using {nickname}: so you don't have any name conflicts with internal functions

import re

# Calculates user input
def calculate(msg, user, channel):
    if msg.startswith('.c'):
        return (True, "core/calculate.py", "calculate.py")
    else:
        return (False, None, None)
        
# Searches google and returns top hit
def search(msg, user, channel):
    if msg.startswith('.g') \
    or msg.startswith('.gc') \
    or msg.startswith('.gcs'):
        return (True, "core/search.py", "search.py")
    else:
        return (False, None, None)
        
# Example Isles

# Echo a message 10 seconds later
def subprocess(msg, user, channel):
    if re.search('example', msg) != None:
        return (True, "examples/subprocess.py", "subprocess.py")
    else:
        return(False, None, None)
    
isles = [
    calculate,
    search,
    subprocess,
]