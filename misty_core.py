#!/usr/bin/env python
# Copyright (C) 2011 Michael Ranieri <michael.d.ranieri at gmail.com>

# System imports
import time
import sys
import random
import os
import re
import json

# Twisted imports
from twisted.words.protocols import irc
from twisted.internet import reactor, protocol, defer
from twisted.python import log
from twisted.enterprise import adbapi

# Misty Imports
import lighthouse
import settings_local as settings


def _getMessage(txn, arg):
    txn.execute("SELECT * FROM Messages WHERE %s" % arg)
    result = txn.fetchall()
    if result:
        return result
    else:
        return None
    
    
# Get a message from PostgreSQL Asynchronously
def getMessage(arg):
    return cp.runInteraction(_getMessage, arg)
    
    
def _setMessage(txn, message, user, channel, id):
    txn.execute('INSERT INTO Messages VALUES (%s, %s, %s, %s)', (message, user, channel, id))
    return

    
# Store a message into PostgreSQL Asynchronously
def setMessage(message, user, channel, id):
    log.msg('%s -- %s: %s' % (channel, user, message))
    return cp.runInteraction(_setMessage, message, user, channel, id)
    
    
# Main class for Misty Bot. Handles messages, connections, etc.
class Misty(irc.IRCClient):
    """A asynchronous IRC Bot."""
    
    nickname = settings.NICKNAME    # nickname for Misty in irc channel
    if settings.PASSWORD:
        password = settings.PASSWORD    # password to join irc server
        
    users = {}
    
    def connectionMade(self):
        log.msg('Connected to server')
        irc.IRCClient.connectionMade(self)
        self.reload()
        
    def connectionLost(self, reason):
        irc.IRCClient.connectionLost(self, reason)
    
    # Reloads the lighthouse module, which points to the isles.
    def reload(self):
        log.msg('Reloading lighthouse')
        reload(lighthouse)
        self.isles = lighthouse.isles
        
    # callbacks for events
    
    def signedOn(self):
        """Called when Misty has successfully signed on to a server."""
        self.join(self.factory.channel)
        
    def joined(self, channel):
        """Called when Misty has joined a channel."""
        log.msg('Connected to channel %s' % channel)
        self.who()
        msg = "Hi! I'm Misty. Nice to meet all of you!"
        self.msg(channel, msg)
        
    def userJoined(self, user, channel):
        """Called when another user joins the channel"""
        log.msg('%s joined %s' % (user, channel))
        self.users[user] = 'H'
        
    def userLeft(self, user, channel):
        """Called when another user leaves the channel"""
        log.msg('%s left %s' % (user, channel))
        self.users[user] = 'G'
        
    def userRenamed(self, oldname, newname):
        """Called when another user changes their name"""
        log.msg('%s changed name to %s' % (oldname, newname))
        self.users[oldname] = 'G'
        self.users[newname] = 'H'
        
    def privmsg(self, user, channel, msg):
        """This will get called when the bot receives a message from IRC server."""
        user = user.split('!', 1)[0]
        
        # Appends a random int to the end of a timestamp in the form of seconds since Epoch.
        # This does have a very small chance of making a non unique id.
        randint = str(random.getrandbits(50))
        timestamp = str(int(time.time()))
        id = timestamp + "!" + randint
        
        # Stores the current message into PostgreSQL
        if settings.USE_DATABASE:
            setMessage(msg, user, channel, id)
        
        # Reload lighthouse
        if msg.startswith(self.nickname + ":reload"):
            msg = "Finding more Isles in the Mist."
            self.msg(channel, msg)
            self.reload()
            return
        
        # Credit
        if msg.startswith(self.nickname + ":"):
            msg = "%s: Hi, I'm %s. Michael Ranieri created me." % (user, self.nickname)
            self.msg(channel, msg)
            return
        
        # Display Help from lighthouse method doc.
        if re.search('help', msg, re.IGNORECASE):
            self.msg(user, "Requirements of message || Result of Isle")
            for isle in self.isles:
                if isle.__doc__:
                    self.msg(user, isle.__doc__)
        
        # params is sent as a tuple to lighthouse and as a json string to the Isles
        # In your Isle you must json.loads(sys.argv[1]) in order to get the params below
        params = (msg, user, channel, self.users)
        
        # Check to see if message should be sent to an isle
        # Isles must return location or None
        for isle in self.isles:
            
            location = isle(params)
            if location:
            
                filename = re.search('([^/]+)$', location).group(0)
            
                log.msg('Sending msg to Isle at:')
                log.msg(location)
                
                # Initialize Process Controller
                MistyProcess = MistyProcessController()
                
                p = reactor.spawnProcess(
                    MistyProcess,                       # Process Controller
                    settings.PATH_TO_ISLES + location,  # Full Path of Isle
                    [filename, json.dumps(params)],     # Filename of Isle, JSON parameters
                    env = _env)                         # ENV to run Isle
                 
                isleResult = MistyProcess.deferred
                isleResult.addCallback(self.callbackMessage, channel)
                
    # Twisted command extension
    def who(self):
        log.msg('Grabbing list of users')
        self.sendLine('WHO *')
        
    def irc_RPL_WHOREPLY(self, prefix, params):
        log.msg(params)
        self.users[params[5]] = params[6]
                
    # method to switch callbacks argument ordering
    def callbackMessage(self, msg, channel):
        self.msg(channel,msg)  
            
    
# Creates instances of Misty for each connection
class MistyFactory(protocol.ClientFactory):
    """A Factory for Misty instances
    
    A new protocol instance of Misty will be created each time we connect to the server(s)
    """
    
    # Misty class will be the protocol to build when new connection is made
    protocol = Misty
    
    def __init__(self, channel):
        self.channel = channel
        
    def startedConnecting(self, connector):
        """Called when Misty is trying to connect to server"""
        log.msg("Trying to connect to IRC server")
        
    def clientConnectionLost(self, connector, reason):
        """If Misty gets disconnecte, reconnect to server."""
        log.msg('Connection lost to IRC server. Will try to reconnect.')
        connector.connect()
        
    def clientConnectionFailed(self, connector, reason):
        log.msg("Could not connect to server:")
        log.msg(reason)
        reactor.stop()
        
        
# Controls the subprocess for each Isle
class MistyProcessController(protocol.ProcessProtocol):
    """A Process Controller that uses ProcessProtocol to handle pipes asynchronously"""
    
    def __init__(self):
        self.data = ""
        self.errors = ""
        self.deferred = defer.Deferred()
    
    # Misty sends msg through arg instead of Stdin
    # so we immediately tell the process to close Stdin
    def connectionMade(self):
        log.msg('Connection made to subprocess')
        self.transport.closeStdin()

    # outRecieved() is called with the output from each Isle process.
    def outReceived(self, data):
        self.data += data
    
    # any errors recieved from Isle process is caught here.
    def errReceived(self, data):
        self.errors += data
        
    # called when process closes its Stdin
    def inConnectionLost(self):
        pass
    
    # This is called when the Isle process has finished and closes its Stdout
    def outConnectionLost(self):
        pass
    
    # This is called when the Isle process has closed the error output.
    def errConnectionLost(self):
        pass
    
    def processExited(self, reason):
        pass
    
    # This is called after the Isle process has ended
    def processEnded(self, reason):
        log.msg('Subprocess Ended:')
        log.msg(reason)
        
        if self.errors != "":
            log.err(self.errors)
        
        self.deferred.callback(self.data)
    

if __name__ == '__main__':
    
    # Allows passing a modified PYTHONPATH to child process
    _env = dict(os.environ)
    _dir = os.path.join(os.path.dirname(__file__))
    try:
        temp = _env['PYTHONPATH']
        temp += ':'
    except:
        temp = ""
    _env['PYTHONPATH'] = str(temp) + str(_dir)
    
    # Open file for logging
    log.startLogging(open('misty.log', 'w'))
    
    # create factory protocol and application 
    mf = MistyFactory(settings.CHANNEL)
    
    if settings.USE_DATABASE:
        # create connection pool for misty to log messages to database
        cp = adbapi.ConnectionPool("pyPgSQL.PgSQL",
                                   None,
                                   settings.DATABASE_USER,
                                   settings.DATABASE_PASSWORD,
                                   settings.DATABASE_URL,
                                   settings.DATABASE_NAME)
    
    # connect factory to this host and port
    reactor.connectTCP(settings.SERVER,
                       settings.PORT,
                       mf)
    
    # run Misty
    reactor.run()