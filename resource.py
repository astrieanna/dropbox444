import os
import os.path as o
import mimetypes
import datetime
import base64

class Resource:
    def initFromUrl(self, url):
        self.url = url

        # use path
        path = urlToPath(url).rstrip('/')
        assert(o.exists(path))
        self.name = o.basename(path)

        # use normpath
        path = o.normpath(path).rstrip('/')
        self.path = path

        self.category = 'directory' if o.isdir(path) else 'file'
        if(self.category == 'directory'):
            self.numItems = len(os.listdir(path))
        else:
            self.size = o.getsize(path)
        self.resourceDate = datetime.datetime.utcfromtimestamp(o.getmtime(path))
        self.resourceType = mimetypes.guess_type(path)[0]

    def addPath(self):
        self.path = o.normpath(urlToPath(self.url).rstrip('/')).rstrip('/')

    def addContent(self, path=False):
        if path == False:
            path = self.path
        self.encoding = "Base64"
        file = open(path, "rb")
        self.content = base64.b64encode(file.read())
        file.close()

    def putContent(self, path):
        print "Category:", self.category
        if self.category == 'directory':
            os.mkdir(path)
        else:
            if not self.encoding == "Base64":
                raise Exception("Only Base64 encoding is supported.")
            file = open(path, "wb")
            file.write(base64.b64decode(self.content))
            file.close()
        
    def deleteContent(self):
        if self.category == "file":
            os.remove(self.path)
        else:
            os.removedirs(self.path)

def urlToPath(url):
    return url.split('/',3)[3]

def splitUrl(url):
    path = urlToPath(url)
    front = url[0: len(url) - len(path) - 1]
    print front, path
    return (front, path)

def getResourceList(url):
    url = url.rstrip('/')
    (front, path) = splitUrl(url)
    path = o.normpath(path)
    assert(o.isdir(path))
    resourceList = []
    files = os.listdir(path)
    if not o.dirname(path) == '':
        files.insert(0, '..')
    for file in files:
        file = path +'/'+ file
        r = Resource()
        r.initFromUrl(front + '/' + file)
        resourceList.append(r)
    return resourceList
