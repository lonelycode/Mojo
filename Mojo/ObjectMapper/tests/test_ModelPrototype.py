import unittest
from datetime import datetime
from Mojo.ObjectMapper.Fields import StringField, IntegerField, BooleanField, FloatField, ListField, ObjectIDField, DateTimeField
from Mojo.ObjectMapper.ModelPrototype import Model


class testModel(Model):
    _id = ObjectIDField()
    title = StringField()
    date_published = DateTimeField()
    published = BooleanField(default=True)
    integer_field = IntegerField()
    float_field = FloatField()
    list_field = ListField()

insert_data = {
    'title':u'test title',
    'date_published': datetime(2012, 1, 1, 1,1,1),
    'published': True,
    'integer_field': 42,
    'float_field': 3.14,
    'list_field': [u'life',u'the universe', u'everything']
}


class TestModelPrototype(unittest.TestCase):

    def test_model_instantiate_from_dict(self):
        testInstantiatedModel = testModel(insert_data)

        self.assertEqual(testInstantiatedModel.title, insert_data['title'])

    def test_attr_access_on_model(self):
        testInstantiatedModel = testModel(insert_data)

        self.assertEqual(testInstantiatedModel.title, insert_data['title'])
        self.assertEqual(testInstantiatedModel.date_published, insert_data['date_published'])
        self.assertEqual(testInstantiatedModel.published, insert_data['published'])
        self.assertEqual(testInstantiatedModel.integer_field, insert_data['integer_field'])
        self.assertEqual(testInstantiatedModel.float_field, insert_data['float_field'])
        self.assertEqual(testInstantiatedModel.list_field, insert_data['list_field'])

    def test_dict_access_on_model(self):
        testInstantiatedModel = testModel(insert_data)

        self.assertEqual(testInstantiatedModel['title'], insert_data['title'])
        self.assertEqual(testInstantiatedModel['date_published'], insert_data['date_published'])
        self.assertEqual(testInstantiatedModel['published'], insert_data['published'])
        self.assertEqual(testInstantiatedModel['integer_field'], insert_data['integer_field'])
        self.assertEqual(testInstantiatedModel['float_field'], insert_data['float_field'])
        self.assertEqual(testInstantiatedModel['list_field'], insert_data['list_field'])

    def test_list_type_on_model(self):
        class smallModel(Model):
            s_field = StringField()

        sm1 = smallModel()
        sm2 = smallModel()

        sm1.s_field = u'test string 1'
        sm2.s_field = u'test string 2'

        class listTestModel(Model):
            _id = ObjectIDField()
            title = StringField()
            date_published = DateTimeField()
            published = BooleanField(default=True)
            integer_field = IntegerField()
            float_field = FloatField()
            list_field = ListField(of=smallModel)

        new_insert_data = {
            'title':u'test title',
            'date_published': datetime(2012, 1, 1, 1,1,1),
            'published': True,
            'integer_field': 42,
            'float_field': 3.14,
            'list_field': [sm1, sm2]
        }

        instancedModel = listTestModel(new_insert_data)

        self.assertEqual(type(instancedModel.list_field[0]), smallModel)
        self.assertEqual(instancedModel.list_field[0].s_field, u'test string 1')
        self.assertEqual(instancedModel.list_field[1].s_field, u'test string 2')

    def test_model_validation(self):
        new_insert_data = {
            'title':u'test title',
            'date_published': datetime(2012, 1, 1, 1,1,1),
            'published': 'this should not be here',
            'integer_field': 42,
            'float_field': 3.14,
            'list_field': [1,2,3]
        }

        testInstantiatedModel = testModel(new_insert_data)

        self.assertRaises(TypeError, testInstantiatedModel.validate)