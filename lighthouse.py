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

# Grabs wiki page
def wikipedia(params):
    """'.wik' & term | Searches wikipedia for term"""
    
    msg, user, channel, users = params
    
    if msg.startswith('.wik'):
        return "core/wikipedia.py"
    else:
        return None

# Calculates user input
def calculate(params):
    """'.c' || Calculates any argument after '.c'"""
    
    msg, user, channel, users = params
    
    if msg.startswith('.c'):
        return "core/calculate.py"
    else:
        return None
        
# Searches google and returns top hit
def search(params):
    """'.g' or '.gc' or '.gcs' || Searches google with any argument after command."""
    
    msg, user, channel, users = params
    
    if msg.startswith('.g') \
    or msg.startswith('.gc') \
    or msg.startswith('.gcs'):
        return "core/search.py"
    else:
        return None
        
# Report last time Misty saw a user
def seen(params):
    """'.seen' & user || Report last time Misty saw a user."""
    
    msg, user, channel, users = params
    
    if msg.startswith('.seen'):
        return "core/seen.py"
    else:
        return None
        
# Stores a message to send to another user
def store_tell(params):
    """'offline_user: message' || Stores a message to give to offline user."""
    
    msg, user, channel, users = params

    if re.match('([\w-]+): .+', msg):
        return "core/store_tell.py"
    else:
        return None

# Gives message to user on first message from receiver
def send_tell(params):
    return "core/send_tell.py"
    
# Shows all outbound messages from user
def outbox(params):
    """'.outbox' || Shows outbound messages that have yet to be received"""
    
    msg, user, channel, user = params
    
    if msg.startswith('.outbox'):
        return "core/outbox.py"
    else:
        return None
    
# API Isles (Require an api key from respective companies)

# Checks for bugs on Lighthouse Issue Tracking
def lighthouse(params):
    """.lighthouse* or .bug* || Return the Lighthouse Tracker URL of the best match."""
    
    msg, user, channel, users = params
    
    if (msg.startswith('.bug') \
    or msg.startswith('.lighthouse')) \
    and settings.LIGHTHOUSE_KEY:
        return "api/lighthouseTracking.py"
    else:
        return None

# Checks Pingdom status of servers.
def pingdom(params):
    """.pingdom || Returns the status of Pingdom checks."""
    
    msg, user, channel, users = params
    
    if msg.startswith('.pingdom') and settings.PINGDOM_KEY:
        return "api/pingdom.py"
    else:
        return None
    
# Searches rackspace for msg terms and returns more information about server
def rackspace(params):
    """.rackspace & (*ip* or *name*) || Return information about rackspace server."""
    
    msg, user, channel, users = params
    
    if msg.startswith('.rackspace') and settings.RACKSPACE_KEY:
        return "api/rackspace.py"
    else:
        return None

# Searches Pivotal Tracker project for stories in msg and return a url to it
def pivotalTracker(params):
    """.pivotal *terms* || Return the Pivotal Tracker URL of the best match story."""
    
    msg, user, channel, users = params
    
    if msg.startswith('.pivotal') and settings.PIVOTAL_KEY:
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
    wikipedia,
    calculate,
    search,
    seen,
    store_tell,
    send_tell,
    outbox,
    lighthouse,
    pingdom,
    rackspace,
    pivotalTracker,
    #mistyComment,
    #subprocess,
    #json_arg,
]