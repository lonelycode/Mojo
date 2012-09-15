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

        value_list=[1,2,3]
        v2 = []
        for item in value_list:
            t = Tag({'tag_name':item})
            v2.append(t)

        a = Tag({'tag_name':'banana'})
        yield gen.Task(a.save_async)

        for p in v2:
            print p.tag_name

        self.render('test.html', message='Your face')