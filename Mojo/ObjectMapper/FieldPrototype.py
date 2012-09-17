class Field(object):
    """
    ``FieldPrototype.Field`` is a parent class for the Fields exposed in ``ObjectMapper.Fields``,
    Offering base functionality and validation options:
    #. validate_type - validates to ensure the base_type class variable is met
    #. validate_is_null - ensures that the property is not null (if set)

    **Usage:** New Field types will inherit from this class::

        from Mojo.ObjectMapper.FieldPrototype import Field

        #Subclass Field to create a new field type
        class StringField(Field):
            base_type = unicode #Must be set to the base type of object you want to save

            #Define your validation methods here and override the validate function to include them:

            def validate_max_length(self):
                #e.g. let's allow this field to have a maximum length
                if self.max_length != 0:
                    if len(self.value) > self.max_length:
                        raise ValueError('%s must be shorter than %i characters' % (self.__class__.__name__,
                                                                                    self.max_length))
                    else:
                        return True

            def validate(self):
                #Call the parent validation methods
                super(StringField, self).validate()

                #Run our own validation methods
                if self.max_length != 0:
                    self.validate_max_length()

    For a full example see the source for ``Mojo.ObjectMapper.Fields.StringField`` as the above example omits the ``__init__()`` overrides that
    establish required properties.

    When defining fields it is also possible to inherit from an existing field type, for example, the ``FloatField`` field type inherits from
    the ``IntegerField`` type, this means we can chain functionality together for more finer-grained subtypes.

    **Methods to override**

    - ``validate_type``: For example, if you have a subtype you would like to take advantage of or do explicit typecasting, see the source for ``StringField`` which coerces strings to unicode
    - ``validate``: To run your custom value validations
    - ``get_value``: To return the correct value back to the user

    """

    base_type = None

    def __init__(self, value=None, allow_empty=True, default=None, **kwargs):
        """
        Base initialisation - will ensure that the field basics are covered.

        **Parameters**
        - ``value``: holds the raw value that will be validated
        - ``allow_empty``: will enable empty checking, default to True
        - ``default``: enables default value to set on ``get_value()``
        """
        self._value = value
        self.allow_empty = allow_empty
        self.default = default


    def _getValue( self ):
        return self.get_value()
    def _setValue( self, value ):
        self._value = value

    value = property( _getValue, _setValue )

    def validate_type(self):
        """
        Basic type validation, this is not strict - it will validate subtypes as well, override this
        if you want to add coercion to your model (see the ``StringField`` and ``FloatField`` for an example)
        """
        if isinstance(self._value, self.base_type):
            return True
        else:
            if self.allow_empty:
                if self._value == None:
                    return True

            raise TypeError("Value for %s must be %s (input was %s)" % (self.__class__.__name__, str(self.base_type), str(type(self._value))))

    def validate_is_null(self):
        """
        Validates if the value is empty. Will throw ``ValueError`` if ``allow_empty`` is false.
        """
        if not self.allow_empty:
            if not self._value:
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
        ``__str__`` and ``__unicode__`` to change this behaviour.
        """

        if self._value:
            self.validate()
            return self._value
        else:
            if self.default:
                return self.default
            else:
                return None

    def __repr__(self):
        return self

    def __unicode__(self):
        return unicode(self._value)

    def __str__(self):
        return str(self._value)

    def __len__(self):
        if self._value:
            return len(self._value)
        else:
            return 0