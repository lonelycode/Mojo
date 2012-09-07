class Field(object):
    """
    FieldPrototype is a parent class for the Fields exposed in Fields.py,
    Offering base functionality and validation options:
    1. validate_type
    2. validate_is_null

    Usage: New Field types will most likely inherit from this class.
    """
    base_type = None

    def __init__(self, value=None, allow_empty=True, default=None, **kwargs):
        """
        value holds the raw value that will be validated
        allow_empty will enable empty checking, default to True
        """
        self.value = value
        self.allow_empty = allow_empty
        self.default = default


    def validate_type(self):
        """
        Basic type validation, this is not strict - it will validate subtypes as well, override this
        if you want to add coercion to your model (see the StringField and FloatField for an example)
        """
        if isinstance(self.value, self.base_type):
            return True
        else:
            if self.allow_empty:
                if self.value == None:
                    return True

            raise TypeError("Value for %s must be %s (input was %s)" % (self.__class__.__name__, str(self.base_type), str(type(self.value))))

    def validate_is_null(self):
        """
        Will throw ValueError if allow_empty is false
        """
        if not self.allow_empty:
            if not self.value:
                raise ValueError('Value of %s cannot be empty' % self.__class__.__name__)
            else:
                return True

    def validate(self):
        """
        Will run all the validation rules, traditionally this will be overridden in a field class
        depending on what validation logic has been added to the Field
        """
        if self.allow_empty == False:
            self.validate_is_null()

        self.validate_type()

    def get_value(self):
        """
        Returns the value stored in the field (string representations will be shown if you print the model, override
        __str__ and __unicode__ to change this behaviour.
        """
        if self.value:
            return self.value
        else:
            if self.default:
                return self.default
            else:
                return None

    def __repr__(self):
        return str(self)

    def __unicode__(self):
        return unicode(self.value)

    def __str__(self):
        return str(self.value)