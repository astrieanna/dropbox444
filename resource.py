import os
import os.path as o
import mimetypes
import datetime
import base64
from shutil import rmtree
from urllib import quote, unquote

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

    def initFromPath(self, path):
        # use path
        if o.exists(path):
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
            rmtree(self.path)

def urlToPath(url):
    return unquote(url.split('/',3)[3])

def splitUrl(url):
    lame_path = url.split('/',3)[3]
    path = urlToPath(url)
    front = url[0: len(url) - len(lame_path) - 1]
    return (front, path)

def getResourceList(url):
    url = url.rstrip('/')
    (front, path) = splitUrl(url)
    path = unquote(path)
    path = o.normpath(path)
    assert(o.isdir(path))
    resourceList = []
    files = os.listdir(path)
    if not o.dirname(path) == '':
        back = Resource()
        backURL = front + '/' + quote(o.normpath(path + '/' + '..'))
        back.initFromUrl(backURL)
        back.name = '..'
        resourceList.append(back)
    for file in files:
        file = quote(path) +'/'+ quote(file)
        r = Resource()
        r.initFromUrl(front + '/' + file)
        resourceList.append(r)
    return resourceList
