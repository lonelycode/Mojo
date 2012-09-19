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
        from bson.objectid import ObjectId

#        newPost = BlogPost()
#        newPost.title = 'THIS TITLE'
#        newPost.slug = 'slugger'
#        newPost.post_body = 'This is a body'
#        newPost.post_intro = 'This is the intro'
#
#        new_tag = Tag()
#        new_tag.tag_name = 'TESTIT'
#
#        newPost.tags = [new_tag]
#
#        yield gen.Task(newPost.save_async)


#        print 'TYPE:', type(Tag.__class__)
#
#        thisPost = yield gen.Task(BlogPost.find_one_async, {'_id':ObjectId('50571e5f3d941cdc4487bdf4')})
#
#        print 'New Tag Test (tag_name): '
#        new_tag = Tag()
#        new_tag.tag_name = 'BLORGYBARGYBANANAFASTAMANDOLA'
#        new_tag2 = Tag()
#        new_tag2.tag_name = 'BLOMMBER'
#        print 'DOT: ', new_tag.tag_name
#        print 'DICT: ', new_tag['tag_name']
#
#        print "-----------------------"
#
#        print 'DOT: ', new_tag2.tag_name
#        print 'DICT: ', new_tag2['tag_name']
###
#        new_tags = thisPost.tags
#        if new_tags:
#            new_tags.append(new_tag)
#        else:
#            new_tags = [new_tag]
#        thisPost.tags = new_tags
#
#        print "======================="
#        for item in thisPost.tags:
#            print 'DOT: ', item.tag_name
#            print 'DICT: ', item['tag_name']
#            print "    ***    "
#
#        print "Get Value test"
#        print "=============="
#        print 'Get_value():', thisPost.get_value()
#        print 'Direct: ', thisPost.tags
#
#        thisPost.tags[0].tag_name = 'BANANAPHONE'
#
#        print 'LISTING TEST:'
#        print thisPost.tags
#        for t in thisPost.tags:
#            print t.tag_name
#
#        print 'SAVING TEST: '
#        yield gen.Task(thisPost.save_async)
#
        thisPost2 = yield gen.Task(BlogPost.find_one_async, {'_id':ObjectId('5059fb6b3d941cdc4487bdff')}) #yield gen.Task(BlogPost.find_async, {})
        thisPost2.tags = []
        yield gen.Task(thisPost2.save_async)
#
#        print 'TAGS:'
#        for t in thisPost2.tags:
#            print t.tag_name
#
#        print 'TITLE:'
#        print thisPost2.title
#
#        print 'LIST TEST:'
#        thesePosts = yield gen.Task(BlogPost.find_async, {})
#
#
#        for item in thesePosts:
#
#
#            if item.title == 'THIS IS A NEW SAVED ITEM':
#                print "FOUND THE ONE"
#
#                print 'FOUND ITEM: ',item
#
#                item.tags = []
#                item.post_intro = 'WHACKJOB'
#                yield gen.Task(item.save_async)
#
#                thisPost3 = yield gen.Task(BlogPost.find_one_async, {'_id':item._id})
#                print "REFOUND ITEM: ", thisPost3
#                print "REFOUND ITEM TITLE: ", thisPost3.title
#                print "REFOUND ITEM TAGS: ", thisPost3.tags
#
#                break







class myFormRequestHandler(MojoRequestHandler, MojoAuthMixin, SessionMixin_Async):
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