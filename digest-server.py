#!/usr/bin/python

import tornado.ioloop
import tornado.web
from curtain import digest
from os import path as ospath

def validate(path, username):
    realpath =ospath.realpath(path)
    print realpath.startswith('/' + username)
        
class Handler(digest.DigestAuthMixin, tornado.web.RequestHandler):
    creds = {}
    def getcreds(uname):
       if uname in Handler.creds:
          return Handler.creds[uname]

    @digest.digest_auth('realm',getcreds)
    def get(self):
        self.write("Username = " + self.params['username'] + "\n")
        validate(self.request.path, self.params['username'])
        self.write("Hello, world digest")

Handler.creds= {}
(user,pw) = ('sampleuser','samplepw')
Handler.creds[user] = {'auth_username': user, 'auth_password': pw}  

application = tornado.web.Application([
    (r"/.*", Handler),
], '')

application.listen(8887)
tornado.ioloop.IOLoop.instance().start()

