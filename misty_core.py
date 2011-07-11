#!/usr/bin/env python
# Copyright (C) 2011 Michael Ranieri <michael.d.ranieri at gmail.com>

# Twisted imports
from twisted.words.protocols import irc
from twisted.internet import reactor, protocol, defer
from twisted.python import log
from twisted.enterprise import adbapi

# System imports
import time, sys, random, os, re, json

# Misty Imports
import lighthouse
import settings_local as settings


# END OF IMPORTS

def _getMessage(txn, arg):
    txn.execute("SELECT * FROM Messages WHERE %s") % arg
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
    return cp.runInteraction(_setMessage, message, user, channel, id)
    
# Main class for Misty Bot. Handles messages, connections, etc.
class Misty(irc.IRCClient):
    """A asynchronous IRC Bot."""
    
    nickname = settings.NICKNAME    # nickname for Misty in irc channel
    password = settings.PASSWORD    # password to join irc server
    users = {}
    
    def connectionMade(self):
        irc.IRCClient.connectionMade(self)
        self.reload()
        
    def connectionLost(self, reason):
        irc.IRCClient.connectionLost(self, reason)
    
    # Reloads the lighthouse module, which points to the isles.
    def reload(self):
        reload(lighthouse)
        self.isles = lighthouse.isles
        
    # callbacks for events
    
    def signedOn(self):
        """Called when Misty has successfully signed on to a server."""
        print 'Connected to server'
        self.join(self.factory.channel)
        
    def joined(self, channel):
        """Called when Misty has joined a channel."""
        self.who()
        msg = "Hi! I'm Misty. Nice to meet all of you!"
        self.msg(channel, msg)
        
    def userJoined(self, user, channel):
        """Called when another user joins the channel"""
        self.users[user] = 'H'
        
    def userLeft(self, user, channel):
        """Called when another user leaves the channel"""
        self.users[user] = 'G'
        
    def userRenamed(self, oldname, newname):
        """Called when another user changes their name"""
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
        setMessage(msg, user, channel, id)
        
        # Reload lighthouse
        if msg.startswith(self.nickname + ":reload"):
            msg = "Finding more Isles in the Mist."
            self.msg(channel, msg)
            self.reload()
            return
        
        if msg.startswith(self.nickname + ":"):
            msg = "%s: Hi, I'm %s. Michael Ranieri created me." % (user, self.nickname)
            self.msg(channel, msg)
            return
        
        # params is sent as a tuple to lighthouse and as a json string to the Isles
        # In your Isle you must json.loads(sys.argv[1]) in order to get the params below
        params = (msg, user, channel, self.users)
        
        # Check to see if message should be sent to an isle
        # Isles must return a tuple (bool, string, string)
        for isle in self.isles:
            goto, location, filename = isle(params)
            if goto == True and filename != None and location != None:
                
                # Initialize Process Controller
                MistyProcess = MistyProcessController()
                
                p = reactor.spawnProcess(
                    MistyProcess,                       # Process Controller
                    settings.PATH_TO_ISLES + location,  # Full Path of Isle
                    [filename, json.dumps(params)],     # Filename of Isle, JSON parameters
                    {'HOME': os.environ['HOME']})       # ENV to run Isle
                 
                isleResult = MistyProcess.deferred
                isleResult.addCallback(self.callbackMessage, channel)
                
    # Twisted command extension
    def who(self):
        self.sendLine('WHO *')
        
    def irc_RPL_WHOREPLY(self, prefix, params):
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
        print "Trying to connect"
        
    def clientConnectionLost(self, connector, reason):
        """If Misty gets disconnecte, reconnect to server."""
        connector.connect()
        
    def clientConnectionFailed(self, connector, reason):
        print "Could not connect to server:", reason
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
        if self.errors != "":
            print "Errors:"
            print self.errors
    
    def processExited(self, reason):
        pass
    
    # This is called after the Isle process has ended
    def processEnded(self, reason):
        self.deferred.callback(self.data)
    

if __name__ == '__main__':
    
    # create factory protocol and application 
    mf = MistyFactory(settings.CHANNEL)
    
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