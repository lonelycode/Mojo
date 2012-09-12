from FieldPrototype import Field
import logging


class StringField(Field):
    """
    Unicode string field for text based storage.

    **Validation methods**

    - ``max_length``: Checks for the maximum length of the string, raises ValueError if not met.

    """
    base_type = unicode

    def __init__(self, *args, **kwargs):
        self.max_length = False

        if 'max_length' in kwargs.keys():
            self.max_length = kwargs['max_length']

        super(StringField, self).__init__(*args, **kwargs)

    def validate_max_length(self):
        if self.max_length != 0:
            if len(self.value) > self.max_length:
                raise ValueError('%s must be shorter than %i characters' % (self.__class__.__name__, self.max_length))
            else:
                return True

    def validate_type(self):
        if isinstance(self.value, self.base_type):
            return True

        elif type(self.value) == str:
            self.value = unicode(self.value)
            logging.warning('Coerced input value to unicode from string')
            return True

        else:
            if self.allow_empty:
                if self.value == None:
                    return True

                try:
                    logging.warning('Type does not match, coercing to unicode string anyway.')
                    self.value = unicode(self.value)
                except:
                    raise TypeError("Value for %s must be %s (input was %s)" % (self.__class__.__name__, str(self.base_type), str(type(self.value))))

    def validate(self):
        super(StringField, self).validate()

        if self.max_length != 0:
            self.validate_max_length()

class IntegerField(Field):
    """
    Stores integer (``int``) data.

    **Validation methods**

    - ``max_value``: maximum value of the integer
    - ``min_value``: minimum value of the stored value

    """
    base_type = int

    def __init__(self, *args, **kwargs):
        self.max_value = False
        self.min_value = False

        if 'max_value' in kwargs.keys():
            self.max_value = kwargs['max_value']

        if 'min_value' in kwargs.keys():
            self.min_value = kwargs['min_value']

        super(IntegerField, self).__init__(*args, **kwargs)

    def validate_max(self):
        if self.max_value:
            if self.value > self.max_value:
                raise ValueError("%s cannot be greater than %i" % (self.__class__.__name__, self.max_value))
            else:
                return True
        else:
            return True

    def validate_min(self):
        if self.min_value:
            if self.value < self.min_value:
                raise ValueError("%s cannot be less than %i" % (self.__class__.__name__, self.min_value))
            else:
                return True
        else:
            return True

    def validate(self):
        super(IntegerField, self).validate()

        if self.min_value:
            self.validate_min()

        if self.max_value:
            self.validate_max()

class BooleanField(Field):
    """
    Stores True or False data.

    **Validation methods**

    - *None*

    """
    base_type = bool

class FloatField(IntegerField):
    """
    Stores Float values.

    **Validation methods**

    - Same as ``IntegerField``

    *Note:* Will coerce integers into float values.
    """
    base_type = float

    def validate_type(self):
        if type(self.value) == self.base_type:
            return True
        elif type(self.value) == int:
            self.value = float(self.value)
            logging.warning('Coerced input value to float from int')
            return True
        else:
            raise TypeError("Value for %s must be %s" % (self.__class__.__name__, str(self.base_type)))


class ListField(Field):
    """
    Stores a list of objects, objects in the list MUST be of type 'Mojo.ObjectMapper.ModelPrototype.Model' as it will
    try to expand and retrieve the relevant value from each on access.

    **Validation methods**

    - *None*

    """
    base_type = list

    def expand_list(self, list):
        ret_list = []
        for item in list:
            val = item.get_value()
            ret_list.append(val)

        return ret_list

    def get_value(self):
        if self.value:
            return self.expand_list(self.value)
        else:
            return None

from bson.objectid import ObjectId
class ObjectIDField(Field):
    """
    ObjectId storage - required for storing data in MongoDB, base type is ``bson.objectid.ObjectId``.

    **Validation methods**

    - *None*

    """
    base_type = ObjectId

    def __repr__(self):
        return self

    def __unicode__(self):
        return unicode(self.value)

    def __str__(self):
        return str(self.value)

from datetime import datetime
class DateTimeField(Field):
    """
    DateTime object storage.

    **Validation methods**

    - *None*

    """
    base_type = datetime