import os
import os.path as o
import mimetypes
import datetime

class Resource:
    def initFromPath(self, path):
        #Should only be called on path that exists
        assert(o.exists(path))
        #strip trailing '/' to accomidate basepath
        path = o.realpath(path).rstrip('/')

        self.category = 'directory' if o.isdir(path) else 'file'
        self.name = o.basename(path)
        if(self.category == 'directory'):
            self.numItems = len(os.listdir(path))
        else:
            self.size = o.getsize(path)
        self.relativePath = path
        self.resourceDate = datetime.datetime.utcfromtimestamp(o.getmtime(path))
        self.resourceType = mimetypes.guess_type(path)[0]


def getResourceList(path):
    assert(o.isdir(path))
    resourceList = []
    #TODO: handle ".." listing (probably elsewhere)
    for file in os.listdir(path):
        r = Resource()
        r.initFromPath(path)
        resourceList.append(r)
    return resourceList
