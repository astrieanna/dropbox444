#!/usr/bin/env python

import httplib2
h = httplib2.Http(".cache")
h.add_credentials('sampleuser', 'samplepw')
resp, content = h.request("http://127.0.0.1:8887/sampleuser/", 
    "GET", body="", 
    headers={'content-type':'text/plain'} )
print content

