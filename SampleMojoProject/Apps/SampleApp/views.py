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

        from Mojo.Forms.MojoFormHelper import model_as_form

        thisForm = model_as_form(BlogPost, ignore=['tags', 'comments'])

        print "Testing unbound:"
        print "================"
        for f in thisForm._fields:
            print "Name: %s Type: %s" % (f, str(type(thisForm._fields[f])))

        thisForm = model_as_form(BlogPost, posts[3], ignore=['tags', 'comments'])

        print "Testing bound:"
        print "=============="
        for f in thisForm._fields:
            try:
                print "Name: %s Type: %s Value: %s" % (f, str(type(thisForm._fields[f])), thisForm._fields[f])
            except:
                print 'Problem on: ', f


        self.render('test.html', message='Your face')

        print "Testing override:"
        print "================="
        from wtforms.fields import TextAreaField
        thisForm = model_as_form(BlogPost, posts[3], ignore=['tags', 'comments'], override={'post_body': TextAreaField, 'post_intro': TextAreaField})
        for f in thisForm._fields:
            try:
                print "Name: %s Type: %s Value: %s" % (f, str(type(thisForm._fields[f])), thisForm._fields[f])
            except:
                print 'Problem on: ', f