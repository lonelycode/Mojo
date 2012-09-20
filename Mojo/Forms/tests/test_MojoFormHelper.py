from datetime import datetime
import unittest
from bson import ObjectId

from Mojo.Forms.MojoFormHelper import Form, model_as_form
from wtforms import BooleanField, TextField, TextAreaField, DateTimeField, HiddenField, IntegerField, FloatField
from Mojo.Backends.PyMongoBackend.pymongo_backend import Session, Collection
from Mojo.ObjectMapper.ModelPrototype import Model
from Mojo.ObjectMapper.Fields import *

DB = Session(host='127.0.0.1', port=27017, db_name='pymongoBackendTest')

class testModel(Model):
    _id = ObjectIDField()
    title = StringField()
    date_published = DateTimeField()
    published = BooleanField()
    integer_field = IntegerField()
    float_field = FloatField()

now = datetime(2012, 1, 1, 1,1,1)

insert_data = {
    'title':u'test title',
    'date_published': now,
    'published': True,
    'integer_field': 42,
    'float_field': 3.14,
}

class blogForm(Form):
    id = HiddenField('id')
    title = TextField('Title')
    post_body = TextAreaField('Post Body')
    date_published = DateTimeField('Published on')
    published = BooleanField('Is published?')
    integer_field = IntegerField()
    float_field = FloatField()

class MojoFormHelperTest(unittest.TestCase):
    def test_populate_from_model(self):
        testInstantiatedModel = testModel(insert_data)
        collectionObj = Collection(DB, testModel)

        #Clear the DB
        allObjects = collectionObj.find({})
        collectionObj.delete(allObjects)
        collectionObj.insert([testInstantiatedModel])

        thisObj = collectionObj.find_one({'title':'test title'})

        thisForm = blogForm.populate_from_model(thisObj)
        collectionObj.delete([thisObj])

        self.assertEqual(thisForm.title.data, thisObj.title)

    def test_populate_model_from_form(self):
        class testForm(Form):
            title = TextField('Title', default='this title')

        class newModel(Model):
            title = StringField()

        thisForm = testForm()
        myModel = thisForm.populate_model_from_data(newModel)

        self.assertEqual(thisForm.title.data, myModel.title)

    def test_model_as_form(self):
        initModel = testModel(insert_data)
        thisForm = model_as_form(testModel, initModel)

        self.assertEqual(thisForm['title'].data, initModel.title)