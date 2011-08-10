#!/usr/bin/env python
from twisted.web.server import Site
from twisted.web.resource import Resource
from twisted.internet import reactor
import json

class FormPage(Resource):
    def render_POST(self, request):
        req = request.__dict__
        content = json.loads(req['content'].getvalue())
        try:
            if content['username'] == 'user' and content['password'] == 'password':
                for m in content['messages']:
                    print m
                return '<html><body>Message Received</body></html>'
            else:
                return '<html><body>Failed Authentication</body></html>'
        except:
            return '<html><body>No username or password</body></html>'
root = Resource()
root.putChild("", FormPage())
factory = Site(root)
reactor.listenTCP(8880, factory)
reactor.run()