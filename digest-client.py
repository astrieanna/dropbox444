#!/usr/bin/env python

import httplib2
h = httplib2.Http(".cache")
h.add_credentials('sampleuser', 'samplepw')
resp, content = h.request("http://10.164.205.69:8887/wat/../sampleuser/yourface", 
    "GET", body="This is text", 
    headers={'content-type':'text/plain'} )
print content

