#!/usr/bin/env python
# Copyright (C) 2011 Michael Ranieri <michael.d.ranieri at gmail.com>

# This file has the settings for Misty Bot.
# Duplicate this file and rename it as settings_local.py with your changed settings.
# DATABASE must be postgreSQL due to asynchronous calls and the use of pyPgSQL library

# If set to False, Misty will not store any messages in database
USE_DATABASE = False

# Name of database
DATABASE_NAME = "Misty"

# user who owns database
DATABASE_USER = "postgres"

# password to access database
DATABASE_PASSWORD = "some_password"

# URL to access database at
DATABASE_URL = "localhost:5432"

# nickname for Misty in IRC
NICKNAME = "Misty"

# IRC server to connect to
SERVER = "irc.someserver.com"

# Port to connect through
PORT = 6667

# Password for IRC Server Ex. "some_irc_password"
PASSWORD = None

# Channel to join once connected
CHANNEL = "#somechannel"

# Path to Misty folder (absolute)
PATH_TO_MISTY = "/Users/SomeUser/Misty"


# API KEYS

# Lighthouse Tracker
LIGHTHOUSE_KEY = None
LIGHTHOUSE_PROJECT_URL = [
    'http://company.lighthouseapp.com/projects/a-project',
    'http://company.lighthouseapp.com/projects/b-project',
]

# Pingdom
PINGDOM_KEY = None
PINGDOM_USER = None
PINGDOM_PASSWORD = None

# Rackspace
RACKSPACE_KEY = None
RACKSPACE_USER = None

# Pivotal Tracker
PIVOTAL_KEY = None
PIVOTAL_PROJECT = None