import tornado.web
from tornado import gen
from Mojo.RequestHandlers.MojoHandler import MojoRequestHandler

from Mojo.ObjectMapper.ModelPrototype import Model
from Mojo.ObjectMapper.Fields import StringField, ObjectIDField, IntegerField

import time

class messages(Model):
    _id = ObjectIDField()
    msg = StringField()

class myRequestHandler(MojoRequestHandler):
    def get(self):
#        print "Adding new entry!"
#        m = messages({'msg':u'This is not a banana'})
#        n = messages({'msg':u'This is not a banana'})
#        o = messages({'msg':u'This is not a banana'})
#        p = messages({'msg':u'This is not a banana'})
#
#        f = messages.insert([m,n,o,p])
#
#        for i in f:
#            print f


#
#        print 'Finding to delete:'
#        a = messages.find_one({'_id':m._id.get_value()})
#        print 'Found:', a._id
#
#        import time
#        time.sleep(10)
#
#        print 'Changing Value:'
#        a.msg = u'Your face is not a bananaface banana head'
#        a.save()
#
#        time.sleep(10)
#
#        print 'Deleting...'
#        a.delete()
#
#        print 'Finding again:'
#        b = messages.find_one({'_id':a._id.get_value()})
#        print 'Found:', b

#        msgs = messages.find({})
#        for m in msgs:
#            print m
#
#        time.sleep(5)
#        print 'Bulk deleting:'
#        new_msgs = msgs[:3]
#        print len(new_msgs)
#        messages.delete_bulk(new_msgs)

        self.render('test.html', message='Your face')

class asyncHandler(MojoRequestHandler):
    @tornado.web.asynchronous
    @gen.engine
    def get(self):
        from bson.objectid import ObjectId

#        print "Adding new entry!"
#        m = messages({'msg':u'This is not a banana1'})
#        n = messages({'msg':u'This is not a banana2'})
#        o = messages({'msg':u'This is not a banana3'})
#        p = messages({'msg':u'This is not a banana4'})
#
#        yield gen.Task(messages.insert_async,[m,n,o,p])


#        print "Adding new entry!"
#        m = messages()
#        m.msg = u'This is not a banana 10'
#        m._id = ObjectId('5049c276e0fba5f11e4dbcaf')

#        whatever = yield gen.Task(m.save_async)

#        print 'Finding to delete:'
#        a = yield gen.Task(messages.find_async, {})
#
#        for i in a:
#            print 'Found: ', i
#
#        to_delete = a[:3]
#        print 'Bulk Deleting'
#        b = yield gen.Task(messages.delete_bulk_async, to_delete)

#
#        import time
#        time.sleep(10)
#
#        print 'Changing Value:'
#        a.msg = u'Your face is not a bananaface banana head'
#        a.save()
#
#        time.sleep(10)
#
#        print 'Deleting...'
#        a.delete()
#
#        print 'Finding again:'
#        b = messages.find_one({'_id':a._id.get_value()})
#        print 'Found:', b

        self.render('test.html', message='Your face')