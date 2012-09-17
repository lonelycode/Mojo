from Mojo.RequestHandlers.MojoHandler import MojoRequestHandler
from Mojo.Auth.Mixins.MojoAuthMixin import MojoAuthMixin
from Mojo.Auth.Mixins.SessionMixins import SessionMixin_Async
from models import *

from tornado import gen
import tornado.web

class myRequestHandler(MojoRequestHandler, MojoAuthMixin, SessionMixin_Async):
    @gen.engine
    @tornado.web.asynchronous
    def get(self):

        posts = yield gen.Task(BlogPost.find_async, {'published':True}, sort=[('date_published',1)])

        for p in posts[:3]:
            print p._id
            print p.title
            print p.post_intro
            print p.date_published.day

            print p



        self.render('test.html', message='Your face')