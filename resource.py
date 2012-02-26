import os
import os.path as o
import mimetypes
import datetime

class Resource:
    def initFromUrl(self, url):
        print "in initFromUrl: url = %s" % (url)
        path = urlToPath(url) 
        print "urlToPath: %s" % (path)
        print path
        #Should only be called on path that exists
        assert(o.exists(path))
        #strip trailing '/' to accomidate basepath
        realpath = o.realpath(path).rstrip('/')

        self.category = 'directory' if o.isdir(realpath) else 'file'
        self.name = o.basename(realpath)
        if(self.category == 'directory'):
            self.numItems = len(os.listdir(realpath))
        else:
            self.size = o.getsize(realpath)
        self.url = url
        self.path = path
        self.resourceDate = datetime.datetime.utcfromtimestamp(o.getmtime(realpath))
        self.resourceType = mimetypes.guess_type(realpath)[0]

    def addConent(self):
        self.encoding = "Base64"
        with open(self.path, "r") as file:
            self.content = base64.b64encode(file.read())

def urlToPath(url):
    return url.split('/',3)[3]

def splitUrl(url):
    path = urlToPath(url)
    front = url[0: len(url) - len(path) - 1]
    print front, path
    return (front, path)


def getResourceList(url):
    (front, path) = splitUrl(url)
    assert(o.isdir(path))
    resourceList = []
    #TODO: handle ".." listing (probably elsewhere)
    for file in os.listdir(path):
        file = o.normpath(path +'/'+ file)
        r = Resource()
        r.initFromUrl(front + '/' + file)
        resourceList.append(r)
    return resourceList
