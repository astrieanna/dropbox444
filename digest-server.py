#!/usr/bin/python
from resource import *
from xmlutils import *
import tornado.ioloop
import tornado.web
from curtain import digest
from os import path as ospath

def validate(path, username):
    realpath = ospath.realpath(path)
    return realpath.startswith('/' + username)
        
class Handler(digest.DigestAuthMixin, tornado.web.RequestHandler):
    creds = {}
    def getcreds(uname):
       if uname in Handler.creds:
          return Handler.creds[uname]

    @digest.digest_auth('realm',getcreds)
    def get(self):
        if(not validate(self.request.path, self.params['username'])):
            raise HTTPError(403)

        print "host: %s\tpath: %s" % (self.request.host, self.request.path)

        r = Resource()
        url = "http://" + self.request.host + self.request.path
        r.initFromUrl(url)

        if r.category == 'directory':
            rs = getResourceList(url)
            xmlstr = buildResourceList(rs)
        else:
            xmlstr = buildResourceDownload(r)

        # fullpath
        # split on category
        # self.write("Username = " + self.params['username'] + "\n")
        # self.write("GET:" + self.request.path)
        self.write(xmlstr)

    def put(self):
        self.write("Put:" + self.request)

    def delete(self):
        self.write("Delete:" + self.request)

# TODO: Make password file
Handler.creds= {}
(user,pw) = ('sampleuser','samplepw')
Handler.creds[user] = {'auth_username': user, 'auth_password': pw}  

application = tornado.web.Application([
    (r"/.*", Handler),
], '')

application.listen(8887)
tornado.ioloop.IOLoop.instance().start()

