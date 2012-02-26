#!/usr/bin/python
from resource import *
from xmlutils import *
import tornado.ioloop
import tornado.web
from curtain import digest
from os import path as ospath
from urllib2 import HTTPError

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
    realpath = ospath.realpath(self.request.path)
    return not realpath.startswith('/' + self.params['username'])

def enclosingDirectoryNotFound(self):
    return not ospath.exists('.' + 
            ospath.dirname(self.request.path.rstrip('/')))

def notFound(self):
    return not ospath.exists('.' + self.request.path)

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
        #TODO: need a notFound for the directory it is in
        self.write("Put:" + self.request)


    @digest.digest_auth('realm',getcreds)
    @testPredicate(forbidden, 403)
    @testPredicate(notFound, 404)
    def delete(self):
        r = Resource()
        r.deleteContent()
        self.set_status(200)
        self.finish()

# TODO: Make password file
Handler.creds= {}
(user,pw) = ('sampleuser','samplepw')
Handler.creds[user] = {'auth_username': user, 'auth_password': pw}  

application = tornado.web.Application([
    (r"/.*", Handler),
], '')

application.listen(8887)
tornado.ioloop.IOLoop.instance().start()

