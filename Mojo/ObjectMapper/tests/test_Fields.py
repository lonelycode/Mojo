import unittest
from Mojo.ObjectMapper.Fields import StringField, IntegerField, BooleanField, FloatField, ListField, ObjectIDField, DateTimeField
from Mojo.ObjectMapper.ModelPrototype import Model

class TestFields(unittest.TestCase):
    def test_StringField(self):
        s = StringField()
        s.value = u"test string"

        self.assertEqual(type(s.value), unicode)

        s2 = StringField(max_length=5)
        s2.value = u'123456'
        self.assertRaises(ValueError, s2.validate)

        s3  =StringField(max_length=5)
        s3.value = u'12345'

        failed = False
        try:
            s3.validate()
        except ValueError:
            failed = True

        self.assertEqual(failed, False)

    def test_IntegerField(self):
        i = IntegerField()
        i.value = 42
        self.assertEqual(type(i.value), int)

        i2 = IntegerField(max_value=5)
        i2.value = 6
        self.assertRaises(ValueError, i2.validate)

        i3 = IntegerField(min_value=5)
        i3.value = 4
        self.assertRaises(ValueError, i3.validate)

        i4 = IntegerField(max_value=10, min_value=8)
        i4.value = 11
        self.assertRaises(ValueError, i4.validate)

        i4.value = 7
        self.assertRaises(ValueError, i4.validate)

    def test_BooleanField(self):
        b = BooleanField()
        b.value = 'mojo'
        self.assertRaises(TypeError, b.validate)

    def test_FloatField(self):
        f = FloatField()
        f.value = 'mojo'
        self.assertRaises(TypeError, f.validate)

    def test_ListField(self):
        l = ListField()
        l.value = 'this is not a list'
        self.assertRaises(TypeError, l.validate)

        class ofModel(Model):
            string_field = StringField()

        l2 = ListField(of=ofModel)
        l2.value = [{'string_field':u'test string'}]

        self.assertEqual(type(l2.value[0]), ofModel)

        self.assertEqual(l2.value[0].string_field, u'test string')

    def test_ObjectIDField(self):
        ob = ObjectIDField()
        ob.value = '1234567'
        self.assertRaises(TypeError, ob.validate)

    def test_DateTimeField(self):
        dt = DateTimeField()
        dt.value = '12345678'
        self.assertRaises(TypeError, dt.validate)
