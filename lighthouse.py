#!/usr/bin/env python
# Copyright (C) 2011 Michael Ranieri <michael.d.ranieri at gmail.com>

# input to methods will be a tuple (Message from irc, user who sent msg, channel, known channel users)
# Must return a location or None
# The first string is the relative location of the isle from the settings.PATH_TO_ISLE
# return None when you don't want the Isle to be called

# NOTE: some messages beginning with {nickname}: are reserved for internal functions
# Try to avoid using {nickname}: so you don't have any name conflicts with internal functions

# System imports
import re

# Misty imports
import settings_local as settings

# Core Isles

# Calculates user input
def calculate(params):
    msg, user, channel, users = params
    
    if msg.startswith('.c'):
        return "core/calculate.py"
    else:
        return None
        
# Searches google and returns top hit
def search(params):
    msg, user, channel, users = params
    
    if msg.startswith('.g') \
    or msg.startswith('.gc') \
    or msg.startswith('.gcs'):
        return "core/search.py"
    else:
        return None
        
# Tells a message to another user when they log in or return from away
def store_tell(params):
    msg, user, channel, users = params

    if re.match('([\w-]+): .+', msg):
        return "core/store_tell.py"
    else:
        return None
        
def send_tell(params):
    return "core/send_tell.py"
    
# API Isles (Require an api key from respective companies)

# Checks Pingdom status of servers.
def pingdom(params):
    msg, user, channel, users = params
    
    if re.search('pingdom', msg, re.IGNORECASE) and settings.PINGDOM_KEY:
        return "api/pingdom.py"
    else:
        return None
    
# Searches rackspace for msg terms and returns more information about server
def rackspace(params):
    msg, user, channel, users = params
    
    if re.search('rackspace', msg, re.IGNORECASE) and settings.RACKSPACE_KEY:
        return "api/rackspace.py"
    else:
        return None

# Searches Pivotal Tracker project for stories in msg and return a url to it
def pivotalTracker(params):
    msg, user, channel, users = params
    
    if re.search('pivotal', msg, re.IGNORECASE) and settings.PIVOTAL_KEY:
        return "api/pivotalTracker.py"
    else:
        return None
        
# Example Isles

# Responds when someone says misty
def mistyComment(params):
    msg, user, channel, users = params
    
    if re.search('misty', msg, re.IGNORECASE):
        return "examples/mistyComment.py"
    else:
        return None

# Echo a message 10 seconds later
def subprocess(params):
    msg, user, channel, users = params
    
    if re.search('example', msg, re.IGNORECASE):
        return "examples/subprocess.py"
    else:
        return None

# Echo the json parameters that would be sent to an Isle
def json_arg(params):
    msg, user, channel, users = params
    
    if re.search('example', msg, re.IGNORECASE):
        return "examples/json_arg.py"
    else:
        return None
    
# Make sure to add your Isle method to isles[] 
isles = [
    calculate,
    search,
    #mistyComment,
    #subprocess,
    #json_arg,
    store_tell,
    send_tell,
    pingdom,
    rackspace,
    pivotalTracker,
]