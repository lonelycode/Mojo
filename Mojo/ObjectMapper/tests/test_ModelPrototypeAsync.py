import unittest
from Mojo.ObjectMapper.Fields import StringField, IntegerField, BooleanField, FloatField, ListField, ObjectIDField, DateTimeField
from Mojo.ObjectMapper.ModelPrototype import Model
from datetime import datetime
from tornado.ioloop import IOLoop
from tornado import testing


import Mojo.ServerHelpers.RunServer

class smallModel(Model):
    s_field = StringField()

class as_testModel(Model):
    _id = ObjectIDField()
    title = StringField()
    date_published = DateTimeField()
    published = BooleanField(default=True)
    integer_field = IntegerField()
    float_field = FloatField()
    list_field = ListField(of=smallModel)

sm1 = smallModel()
sm2 = smallModel()
sm1.s_field = u'test string 1'
sm2.s_field = u'test string 2'

new_insert_data = {
    'title':u'test title',
    'date_published': datetime(2012, 1, 1, 1,1,1),
    'published': True,
    'integer_field': 42,
    'float_field': 3.14,
    'list_field': [sm1, sm2]
}

class TestModelAsyncFunctions(testing.AsyncTestCase):

    def get_new_ioloop(self):
        return IOLoop.instance()

    def __setup(self, model):
        from Mojo.Backends.AsyncmongoBackend.asyncmongo_backend import Collection, Session
        Mojo.ServerHelpers.RunServer.BACKEND_COLLECTION = Collection
        Mojo.ServerHelpers.RunServer.DATABASE = Session(host='127.0.0.1', port=27017, db_name='modelPrototypeASYNCTestDB')

        #Clear the DB
        model.find_async({}, callback=self.stop)
        allObjects = self.wait()

        model.delete_bulk_async(allObjects, callback=self.stop)
        ignore = self.wait()


    def test_model_save_async(self):
        self.__setup(as_testModel)

        instancedModel = as_testModel(new_insert_data)
        instancedModel.save_async(callback=self.stop)
        retObj = self.wait()

        as_testModel.find_one_async({'title':u'test title'}, callback=self.stop)
        found = self.wait()

        instancedModel._id = found._id
        instancedModel.delete_async(callback=self.stop)
        retObj = self.wait()

        self.assertEqual(found.title, instancedModel.title)
        self.assertEqual(found.date_published, instancedModel.date_published)
        self.assertEqual(found.published, instancedModel.published)
        self.assertEqual(found.integer_field, instancedModel.integer_field)
        self.assertEqual(found.float_field, instancedModel.float_field)
        self.assertEqual(found.list_field, instancedModel.list_field)

    def test_model_find_async(self):
        self.__setup(as_testModel)



        more_data = new_insert_data = {
            'title':u'other title',
            'date_published': datetime(2012, 2, 2, 1,1,1),
            'published': True,
            'integer_field': 42,
            'float_field': 3.14,
            'list_field': [sm1, sm2]
        }

        other_data = new_insert_data = {
            'title':u'this title',
            'date_published': datetime(2012, 2, 2, 1,1,1),
            'published': True,
            'integer_field': 42,
            'float_field': 3.14,
            'list_field': [sm1, sm2]
        }

        thisModel = as_testModel(more_data)
        thisModel.save_async(callback=self.stop)
        newModel = as_testModel(other_data)
        newModel.save_async(callback=self.stop)

        as_testModel.find_async({}, callback=self.stop)
        retObj = self.wait()

        self.assertEqual(2, len(retObj))
        self.assertEqual(retObj[0].title, more_data['title'])

    def test_model_find_one_async(self):
        self.__setup(as_testModel)

        as_testModel(new_insert_data).save_async(callback=self.stop)
        as_testModel.find_one_async({'title':u'test title'}, callback=self.stop)
        found = self.wait()

        self.assertEqual(found.title, new_insert_data['title'])
        self.assertEqual(found.date_published, new_insert_data['date_published'])
        self.assertEqual(found.published, new_insert_data['published'])
        self.assertEqual(found.integer_field, new_insert_data['integer_field'])
        self.assertEqual(found.float_field, new_insert_data['float_field'])
        self.assertEqual(found.list_field, new_insert_data['list_field'])


    def test_model_delete_async(self):
        self.__setup(as_testModel)

        more_other_data = {
            'title':u'moar titles plz',
            'date_published': datetime(2012, 2, 2, 1,1,1),
            'published': True,
            'integer_field': 42,
            'float_field': 3.14,
            'list_field': [sm1, sm2]
        }

        as_testModel(more_other_data).save_async(callback=self.stop)

        as_testModel.find_one_async({'title':u'moar titles plz'}, callback=self.stop)
        #This is hacky but it ensures the write is clean
        import time
        time.sleep(1)
        newfoundValue = self.wait()
        self.assertEqual(newfoundValue.title, more_other_data['title'])
        self.assertNotEqual(newfoundValue._id, None)

        if newfoundValue:
            newfoundValue.delete_async(callback=self.stop)
            ignore = self.wait()

        as_testModel.find_one_async({'title':u'moar titles plz'}, callback=self.stop)
        not_found = self.wait()

        self.assertEqual(not_found, None)
