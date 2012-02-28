#!/usr/bin/env python

import httplib2
import sys
import xmlutils

h = httplib2.Http(".cache")
h.add_credentials('sampleuser', 'samplepw')
print "http://127.0.0.1:8887/" + sys.argv[1]
resp, content = h.request("http://127.0.0.1:8887/" + sys.argv[1], 
    "GET", body="", 
    headers={'content-type':'text/plain'} )
#(isDir, r) = xmlutils.parseResponse(content)
#r.putContent("downloaded-file")
print content

