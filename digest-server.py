#!/usr/bin/python
from resource import *
from xmlutils import *
import tornado.ioloop
import tornado.web
from curtain import digest
from os import path as ospath
from urllib2 import HTTPError
from urllib import unquote


def chunks(l, n):
    return [l[i:i+n] for i in range(0, len(l), n)]

def testPredicate(pred, errno):
    def testPredicateDecorator(func):
        def newFunc(self):
            if pred(self):
                self.send_error(errno)
            else:
                func(self)
        return newFunc
    return testPredicateDecorator

def forbidden(self):
    realpath = ospath.realpath(unquote(self.request.path))
    return not realpath.startswith('/' + self.params['username'])

def enclosingDirectoryNotFound(self):
    return not ospath.exists('.' + 
            ospath.dirname(unquote(self.request.path).rstrip('/')))

def notFound(self):
    return not ospath.exists('.' + unquote(self.request.path))

class Handler(digest.DigestAuthMixin, tornado.web.RequestHandler):
    creds = {}
    def getcreds(uname):
       if uname in Handler.creds:
          return Handler.creds[uname]


    @digest.digest_auth('realm',getcreds)
    @testPredicate(forbidden, 403)
    @testPredicate(notFound, 404)
    def get(self):

        print "host: %s\tpath: %s" % (self.request.host, self.request.path)

        r = Resource()
        url = self.request.full_url()
        r.initFromUrl(url)

        if r.category == 'directory':
            rs = getResourceList(url)
            xmlstr = buildResourceList(rs)
        else:
            r.addContent()
            xmlstr = buildResourceDownload(r)

        print xmlstr
        self.write(xmlstr)


    @digest.digest_auth('realm',getcreds)
    @testPredicate(forbidden, 403)
    @testPredicate(enclosingDirectoryNotFound, 404)
    def put(self):
        resource = parseResourceUpload(self.request.body)
        # Error if writing uploading a directory where a file exists
        if resource.category == "directory" and not notFound(self):
            return self.send_error(400)
        resource.putContent('.'+ unquote(self.request.path))
        self.set_status(200)
        self.finish()


    @digest.digest_auth('realm',getcreds)
    @testPredicate(forbidden, 403)
    @testPredicate(notFound, 404)
    def delete(self):
        r = Resource()
        url = self.request.full_url()
        r.initFromUrl(url)
        r.deleteContent()
        self.set_status(200)
        self.finish()

passwdfile = open(".passwd", "r")
Handler.creds= {}
for [user, pw] in chunks(passwdfile.readlines(), 2):
    user = user.strip('\n')
    pw = pw.strip('\n')
    Handler.creds[user] = {'auth_username': user, 'auth_password': pw}  

application = tornado.web.Application([
    (r"/.*", Handler),
], '')

application.listen(8887)
tornado.ioloop.IOLoop.instance().start()

