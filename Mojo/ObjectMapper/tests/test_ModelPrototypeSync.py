import unittest
from Mojo.ObjectMapper.Fields import StringField, IntegerField, BooleanField, FloatField, ListField, ObjectIDField, DateTimeField
from Mojo.ObjectMapper.ModelPrototype import Model
from Mojo.Backends.PyMongoBackend.pymongo_backend import Collection, Session
from datetime import datetime
from tornado.ioloop import IOLoop
from tornado import testing

import Mojo.ServerHelpers.RunServer

class smallModel(Model):
    s_field = StringField()

class testModel(Model):
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

class TestModelSyncFunctions(unittest.TestCase):

    def __setup(self, model):
        Mojo.ServerHelpers.RunServer.BACKEND_COLLECTION = Collection
        Mojo.ServerHelpers.RunServer.DATABASE = Session(host='127.0.0.1', port=27017, db_name='modelPrototypeSyncTestDB')
        #Clear the DB
        allObjects = model.find({})
        model.delete_bulk(allObjects)

    def test_model_save(self):
        self.__setup(testModel)

        instancedModel = testModel(new_insert_data)
        retObj = instancedModel.save()

        found = testModel.find_one({'_id':retObj._id})

        instancedModel.delete()

        self.assertEqual(found.title, instancedModel.title)
        self.assertEqual(found.date_published, instancedModel.date_published)
        self.assertEqual(found.published, instancedModel.published)
        self.assertEqual(found.integer_field, instancedModel.integer_field)
        self.assertEqual(found.float_field, instancedModel.float_field)
        self.assertEqual(found.list_field, instancedModel.list_field)

    def test_model_find(self):
        self.__setup(testModel)

        new_insert_data1 = {
            'title':u'test title 1',
            'date_published': datetime(2012, 1, 1, 1,1,1),
            'published': True,
            'integer_field': 42,
            'float_field': 3.14,
            'list_field': [sm1, sm2]
        }

        new_insert_data2 = {
            'title':u'test title 2',
            'date_published': datetime(2012, 1, 1, 1,1,1),
            'published': True,
            'integer_field': 42,
            'float_field': 3.14,
            'list_field': [sm1, sm2]
        }

        new_insert_data3 = {
            'title':u'test title 3',
            'date_published': datetime(2012, 1, 1, 1,1,1),
            'published': True,
            'integer_field': 42,
            'float_field': 3.14,
            'list_field': [sm1, sm2]
        }

        m1 = testModel(new_insert_data1)
        m2 = testModel(new_insert_data2)
        m3 = testModel(new_insert_data3)

        savedObj1 = m1.save()
        savedObj2 = m2.save()
        savedObj3 = m3.save()

        allObjs = testModel.find({})[:]

        self.assertEqual(len(allObjs), 3)
        self.assertEqual(allObjs[0].title, new_insert_data1['title'])
        self.assertEqual(allObjs[1].title, new_insert_data2['title'])
        self.assertEqual(allObjs[2].title, new_insert_data3['title'])


    def test_model_find_one(self):
        self.__setup(testModel)

        instancedModel = testModel(new_insert_data)
        retObj = instancedModel.save()

        found = testModel.find_one({'_id':retObj._id})

        instancedModel.delete()

        self.assertEqual(found.title, instancedModel.title)

    def test_model_delete(self):
        self.__setup(testModel)

        instancedModel = testModel(new_insert_data)
        retObj = instancedModel.save()

        found = testModel.find_one({'_id':retObj._id})

        instancedModel.delete()

        found_empty = testModel.find_one({'_id':retObj._id})

        self.assertEqual(found_empty, None)