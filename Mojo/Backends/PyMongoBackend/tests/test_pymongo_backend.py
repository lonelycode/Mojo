from datetime import datetime
import unittest
from bson import ObjectId

from Mojo.Backends.PyMongoBackend.pymongo_backend import Session, Collection
from Mojo.ObjectMapper.ModelPrototype import Model
from Mojo.ObjectMapper.Fields import *

DB = Session(host='127.0.0.1', port=27017, db_name='pymongoBackendTest')

class AuthManagerTest(unittest.TestCase):

    def test_find_insert_find_one_delete(self):
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
        allObjects = collectionObj.find({})

        ignore = collectionObj.delete(allObjects)


        ret_vals = collectionObj.insert([testInstantiatedModel])


        thisObj = collectionObj.find_one({'title':'test title'})

        as_dict = {}
        if thisObj:
            as_dict = dict(thisObj)
            itemID = as_dict['_id']
            del as_dict['_id']

            ignore = collectionObj.delete([thisObj])

        self.assertEqual(as_dict, insert_data)

    def test_save(self):
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
        allObjects = collectionObj.find({})


        ignore =collectionObj.delete(allObjects)


        ret_vals =collectionObj.insert([testInstantiatedModel])



        thisObj =collectionObj.find_one({'title':u'test title'})



        as_dict = {}
        if thisObj:
            thisObj.title = u'consider phlebas'
            thisObj.date_published = now
            thisObj.published = False
            thisObj.integer_field = 43
            thisObj.float_field = 3.15
            thisObj.list_field = None


            save_return = collectionObj.save(thisObj)

            changedObj = collectionObj.find_one({'title':u'consider phlebas'})


            if changedObj:
                as_dict = dict(changedObj)
                del as_dict['_id']

                ignore = collectionObj.delete([changedObj])

        self.assertEqual(as_dict, changed_data)

    def test_delete(self):
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
        allObjects = collectionObj.find({})
        ignore = collectionObj.delete(allObjects)

        ret_vals = collectionObj.insert([testInstantiatedModel])

        thisObj = collectionObj.find_one({'title':u'test title'})

        emptyObj = {'value':True}

        if thisObj:
            ret = collectionObj.delete([thisObj])
            emptyObj = collectionObj.find_one({'title':u'test title'})


        self.assertEqual(emptyObj, None)


if __name__ == '__main__':
    testing.main()