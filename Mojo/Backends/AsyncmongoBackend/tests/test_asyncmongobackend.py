import unittest
from datetime import datetime, timedelta, tzinfo
from tornado.ioloop import IOLoop
from tornado import testing
from bson import ObjectId

from Mojo.Backends.AsyncmongoBackend.asyncmongo_backend import Session, Collection
from Mojo.ObjectMapper.ModelPrototype import Model
from Mojo.ObjectMapper.Fields import *



class AuthManagerTest(testing.AsyncTestCase):
    def get_new_ioloop(self):
        return IOLoop.instance()

    def test_find_insert_find_one_delete(self):
        DB = Session(host='127.0.0.1', port=27017, db_name='asyncmongoBackendTest')
        class testModel(Model):
            _id = ObjectIDField()
            title = StringField()
            date_published = DateTimeField()
            published = BooleanField(default=True)
            integer_field = IntegerField()
            float_field = FloatField()
            list_field = ListField()

        now = datetime(2012, 1, 1, 1,1,1)

        insert_data = {
            'title':u'test title',
            'date_published': now,
            'published': True,
            'integer_field': 42,
            'float_field': 3.14,
            'list_field': [u'life',u'the universe', u'everything']
        }

        testInstantiatedModel = testModel(insert_data)
        collectionObj = Collection(DB, testModel)

        #Clear the DB
        collectionObj.find({}, callback=self.stop)
        allObjects = self.wait()

        collectionObj.delete(allObjects, callback=self.stop)
        ignore = self.wait()

        collectionObj.insert([testInstantiatedModel], callback=self.stop)

        ret_vals = self.wait()

        collectionObj.find_one({'title':'test title'}, callback=self.stop)

        thisObj = self.wait()

        as_dict = {}
        if thisObj:
            as_dict = dict(thisObj)
            itemID = as_dict['_id']
            del as_dict['_id']

            collectionObj.delete([thisObj], callback=self.stop)

            ignore = self.wait()

        self.assertEqual(as_dict, insert_data)

    def test_save(self):
        DB = Session(host='127.0.0.1', port=27017, db_name='asyncmongoBackendTest')
        class testModel(Model):
            _id = ObjectIDField()
            title = StringField()
            date_published = DateTimeField()
            published = BooleanField()
            integer_field = IntegerField()
            float_field = FloatField()
            list_field = ListField()

        now = datetime(2012, 1, 1, 1,1,1)

        insert_data = {
            'title':u'test title',
            'date_published': now,
            'published': True,
            'integer_field': 42,
            'float_field': 3.14,
            'list_field': [u'life',u'the universe', u'everything']
        }

        changed_data = {
            'title':u'consider phlebas',
            'date_published': now,
            'published': False,
            'integer_field': 43,
            'float_field': 3.15,
            'list_field': None
        }

        testInstantiatedModel = testModel(insert_data)
        collectionObj = Collection(DB, testModel)

        #Clear the DB
        collectionObj.find({}, callback=self.stop)
        allObjects = self.wait()

        collectionObj.delete(allObjects, callback=self.stop)
        ignore = self.wait()

        collectionObj.insert([testInstantiatedModel], callback=self.stop)

        ret_vals = self.wait()

        collectionObj.find_one({'title':u'test title'}, callback=self.stop)

        thisObj = self.wait()

        as_dict = {}
        if thisObj:
            thisObj.title = u'consider phlebas'
            thisObj.date_published = now
            thisObj.published = False
            thisObj.integer_field = 43
            thisObj.float_field = 3.15
            thisObj.list_field = None


            collectionObj.save(thisObj, callback=self.stop)
            save_return = self.wait()

            collectionObj.find_one({'title':u'consider phlebas'}, callback=self.stop)

            changedObj = self.wait()

            if changedObj:
                as_dict = dict(changedObj)
                del as_dict['_id']

                collectionObj.delete([changedObj], callback=self.stop)

                ignore = self.wait()

        self.assertEqual(as_dict, changed_data)

    def test_delete(self):
        DB = Session(host='127.0.0.1', port=27017, db_name='asyncmongoBackendTest')
        class testModel(Model):
            _id = ObjectIDField()
            title = StringField()
            date_published = DateTimeField()
            published = BooleanField()
            integer_field = IntegerField()
            float_field = FloatField()
            list_field = ListField()

        now = datetime(2012, 1, 1, 1,1,1)

        insert_data = {
            'title':u'test title',
            'date_published': now,
            'published': True,
            'integer_field': 42,
            'float_field': 3.14,
            'list_field': [u'life',u'the universe', u'everything']
        }


        testInstantiatedModel = testModel(insert_data)
        collectionObj = Collection(DB, testModel)

        #Clear the DB
        collectionObj.find({}, callback=self.stop)
        allObjects = self.wait()

        collectionObj.delete(allObjects, callback=self.stop)
        ignore = self.wait()

        collectionObj.insert([testInstantiatedModel], callback=self.stop)

        ret_vals = self.wait()

        collectionObj.find_one({'title':u'test title'}, callback=self.stop)

        thisObj = self.wait()

        emptyObj = {'value':True}

        if thisObj:
            collectionObj.delete([thisObj], callback=self.stop)
            ret = self.wait()
            collectionObj.find_one({'title':u'test title'}, callback=self.stop)
            emptyObj = self.wait()


        self.assertEqual(emptyObj, None)


if __name__ == '__main__':
    testing.main()