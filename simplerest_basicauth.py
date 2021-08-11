#!/usr/bin/python

from zope.interface import implementer

from twisted.web import guard, resource
from twisted.web.server import Site
from twisted.web.resource import Resource
from twisted.internet import reactor
from twisted.cred.portal import Portal, IRealm
from twisted.cred.checkers import InMemoryUsernamePasswordDatabaseDontUse
import time
import os
import json
import html
import sys


class FormPage(Resource):
    isLeaf = False

    def __init__(self):
        return

    def getChild(self, name, request):
        if name == '':
            return self
        return Resource.getChild(self, name, request)

    def render_POST(self, request):
        request.responseHeaders.addRawHeader(b"content-type", b"text/plain")
        return ("You posted data:\n%s" % (str(request.content.read()),)).encode('utf-8')
   
    def render_GET(self, request):
        request.setHeader("Content-Type", "application/json")
        emp=request.args[b'emp'][0]

        print (request.path)

        resString = ""
        #if request.path == "/apis/redir":
            #resString = "{ \"args\":" + json.dumps(str(request.args)) + "}"
        #elif emp == "1":
        if emp == "1":
            resString = "{ \"employees\": [ { \"firstName\":\"John\" , \"lastName\":\"Doe\" } ], \"args\":" + json.dumps(str(request.args)) + "}"
        else :
            resString = "{ \"employees\": [ { \"firstName\":\"Anna\" , \"lastName\":\"Smith\" } ] }"
        
        return resString.encode('utf-8')

class RedirectPoint(Resource):
    def __init__(self):
        return

    def render_GET(self, request):
        request.setHeader("Content-Type", "application/json")

        print (request.path)

        resString = ""
        resString = "{ \"args\":" + json.dumps(str(request.args)) + "}"
        
        return resString.encode()

class RootResource(Resource):
  def __init__(self):
        Resource.__init__(self)
        self.putChild(b"apis", ContextResource())
    
class ContextResource(Resource):
  def __init__(self):
        Resource.__init__(self)
        self.putChild(b"emps", FormPage())
        self.putChild(b"redir", RedirectPoint())

@implementer(IRealm)
class SimpleRealm():
    """
    A realm which gives out L{GuardedResource} instances for authenticated
    users.
    """

    def requestAvatar(self, avatarId, mind, *interfaces):
        if resource.IResource in interfaces:
            return resource.IResource, RootResource(), lambda: None
        raise NotImplementedError()

    
checkers = [InMemoryUsernamePasswordDatabaseDontUse(joe=b'blow')]
#root = Resource()
wrapped_resource = guard.HTTPAuthSessionWrapper(
    Portal(SimpleRealm(), checkers),
    [guard.BasicCredentialFactory(b"example.com")],
)

#context = Resource()
#formPage = FormPage()
#root.putChild(b"apis", context)
#context.putChild(b"redir", RedirectPoint())
#context.putChild(b"emps", formPage)
factory = Site(wrapped_resource)
port = os.environ.get("PORT", "8880")
reactor.listenTCP(int(port), factory)
reactor.run()
