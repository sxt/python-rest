#!/usr/bin/python
from twisted.web.server import Site
from twisted.web.resource import Resource
from twisted.internet import reactor
import time
import os
import json
import html



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
        
        return resString.encode()

class RedirectPoint(Resource):
    def __init__(self):
        return

    def render_GET(self, request):
        request.setHeader("Content-Type", "application/json")

        print (request.path)

        resString = ""
        resString = "{ \"args\":" + json.dumps(str(request.args)) + "}"
        
        return resString

root = Resource()
context = Resource()
formPage = FormPage()
root.putChild(b"apis", context)
context.putChild(b"redir", RedirectPoint())
context.putChild(b"emps", formPage)
factory = Site(root)
port = os.environ.get("PORT", "8880")
reactor.listenTCP(int(port), factory)
reactor.run()
