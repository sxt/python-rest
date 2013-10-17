#!/usr/bin/python
from twisted.web.server import Site
from twisted.web.resource import Resource
from twisted.internet import reactor
import time

import cgi

class FormPage(Resource):
    def __init__(self):
        return

    def render_GET(self, request):
        request.setHeader("Content-Type", "application/json")
        emp=request.args['emp'][0]
        print emp
        resString = ""
        if emp == "1":
            resString = "{ \"employees\": [ { \"firstName\":\"John\" , \"lastName\":\"Doe\" } ] }"
        else :
            resString = "{ \"employees\": [ { \"firstName\":\"Anna\" , \"lastName\":\"Smith\" } ] }"
        
        return resString

root = Resource()
root.putChild("apis", FormPage())
factory = Site(root)
reactor.listenTCP(8880, factory)
reactor.run()
