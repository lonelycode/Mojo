from Fields import *
from tornado import gen
from Mojo.ServerHelpers.RunServer import BACKEND_COLLECTION, DATABASE

class Model(dict):
    """
    Basic Model class that defines the behaviours of Model objects, the class enables simple definition:

    To create  a new model:

    class MyTestModel(Model):
        this_field =        StringField()
        another_field =     IntegerField()
        whatever_field =    BooleanField()

    The class will evaluate validate() on each field when the value is retrieved and maps all values to an
    internal dict (as it subclasses dict) it bahvaes a little like one by enabling [] and dot-style assignment
    to values.

    Models are recursive, so should produce a valid dict with EmbeddedField fields that are nested as they all expose
    the get_value() function.
    """
    def __init__(self, data=None):
        super(Model, self).__init__()

        self.__initialise_dictionary_from_classvars()

        if data:
            self.__instantiate_from_dict(data)

    def get_value(self):
        return self.__get_value()

    def __getattr__(self, name):
        return self.__class__.__dict__[name].get_value()

    def __setattr__(self, name, value):
        if name in self.__data__.keys():
            self.__data__[name] = value
            self.__class__.__dict__[name].value = value
        else:
            raise KeyError('No such key in model')

    def __len__(self):
        #Enables us to be 'falsy'
        return len(self.__get_value())

    __getitem__ = __getattr__
    __setitem__ = __setattr__

    def __initialise_dictionary_from_classvars(self):
        """
        Will intitalise the model's dictionary with the various names of the
        class variables
        """

        cls_var_list = [i for i in self.__class__.__dict__.keys() if '__' not in i and 'collection_name' not in i]

        init_dict = dict()
        for v in cls_var_list:
            init_dict[v] = None

        self.__dict__['__data__'] = init_dict

    def __instantiate_from_dict(self, data):
        """
        Will populate the model from a dictionary passed as a constructor.
        """

        if type(data) == dict:
            for key in data.keys():
                if key in self.__dict__['__data__'].keys():
                    val = data[key]
                    if isinstance(val, dict):
                        model_instance = self.__class__.__dict__[key].to(val)
                        self.__dict__['__data__'][key] = model_instance
                        self.__class__.__dict__[key].value = model_instance
                    else:
                        self.__dict__['__data__'][key] = data[key]
                        self.__class__.__dict__[key].value = data[key]
                else:
                    logging.warning("Ignoring '%s' from input, couldn't find matching model Field entry" % (key) )

        else:
            raise ValueError('Input data to model must be a dictionary')


    def __validate(self):
        """
        Validates the entire model, is called when _get_value() is called.
        """
        value_dict = self.__dict__['__data__']
        for key in value_dict.keys():
            self.__class__.__dict__[key].value = value_dict[key]
            self.__class__.__dict__[key].validate()

    def __get_value(self):
        """
        Return a dictionary of all the members (if it validates)
        """

        self.__validate()

        value_dict = self.__dict__['__data__']
        ret_val = {}
        for key in value_dict:
            if self.__class__.__dict__[key].get_value():
                ret_val[key] = self.__class__.__dict__[key].get_value()

        return ret_val

    @classmethod
    def insert(klass, to_insert):
        from Mojo.ServerHelpers.RunServer import BACKEND_COLLECTION, DATABASE

        if DATABASE:
            if BACKEND_COLLECTION:
                this_collection = BACKEND_COLLECTION(DATABASE, klass)
                ret_obj = this_collection.insert(to_insert)

                return ret_obj

    @classmethod
    @gen.engine
    def insert_async(klass, to_insert, *args, **kwargs):
        from Mojo.ServerHelpers.RunServer import BACKEND_COLLECTION, DATABASE

        cb = kwargs['callback']
        del(kwargs['callback'])

        if DATABASE:
            if BACKEND_COLLECTION:
                this_collection = BACKEND_COLLECTION(DATABASE, klass)
                ret_obj = yield gen.Task(this_collection.insert,to_insert, *args, **kwargs)

                cb(ret_obj)

    def save(self):
        from Mojo.ServerHelpers.RunServer import BACKEND_COLLECTION, DATABASE

        if DATABASE:
            if BACKEND_COLLECTION:
                this_collection = BACKEND_COLLECTION(DATABASE, self)
                ret_obj = this_collection.save(self)

                return ret_obj

    @gen.engine
    def save_async(self, callback):
        from Mojo.ServerHelpers.RunServer import BACKEND_COLLECTION, DATABASE

        if DATABASE:
            if BACKEND_COLLECTION:
                this_collection = BACKEND_COLLECTION(DATABASE, self)
                ret_obj = yield gen.Task(this_collection.save, self)

                callback(ret_obj)

    def delete(self):
        from Mojo.ServerHelpers.RunServer import BACKEND_COLLECTION, DATABASE

        if DATABASE:
            if BACKEND_COLLECTION:
                this_collection = BACKEND_COLLECTION(DATABASE, self)
                ret_obj = this_collection.delete([self])

                return ret_obj

    @classmethod
    def delete_bulk(klass, to_delete):
        from Mojo.ServerHelpers.RunServer import BACKEND_COLLECTION, DATABASE

        if DATABASE:
            if BACKEND_COLLECTION:
                this_collection = BACKEND_COLLECTION(DATABASE, klass)
                ret_obj = this_collection.delete(to_delete)

                return ret_obj

    @classmethod
    @gen.engine
    def delete_bulk_async(klass, to_delete, callback):
        from Mojo.ServerHelpers.RunServer import BACKEND_COLLECTION, DATABASE


        if DATABASE:
            if BACKEND_COLLECTION:
                this_collection = BACKEND_COLLECTION(DATABASE, klass)
                ret_obj = yield gen.Task(this_collection.delete, to_delete)

                callback(ret_obj)

    @gen.engine
    def delete_async(self, callback):
        from Mojo.ServerHelpers.RunServer import BACKEND_COLLECTION, DATABASE

        if DATABASE:
            if BACKEND_COLLECTION:
                this_collection = BACKEND_COLLECTION(DATABASE, self)
                ret_obj = yield gen.Task(this_collection.delete, [self])

                callback(ret_obj)

    @classmethod
    def find(klass, *args, **kwargs):
        from Mojo.ServerHelpers.RunServer import BACKEND_COLLECTION, DATABASE
        klass.collection_name = klass.__name__

        if DATABASE:
            if BACKEND_COLLECTION:
                this_collection = BACKEND_COLLECTION(DATABASE, klass)
                ret_obj = this_collection.find(*args, **kwargs)

                return ret_obj

    @classmethod
    @gen.engine
    def find_async(klass, *args, **kwargs):
        from Mojo.ServerHelpers.RunServer import BACKEND_COLLECTION, DATABASE
        klass.collection_name = klass.__name__

        cb = kwargs['callback']
        del(kwargs['callback'])

        if DATABASE:
            if BACKEND_COLLECTION:
                this_collection = BACKEND_COLLECTION(DATABASE, klass)
                ret_obj = yield gen.Task(this_collection.find, *args, **kwargs)

                cb(ret_obj)

    @classmethod
    def find_one(klass, *args, **kwargs):
        from Mojo.ServerHelpers.RunServer import BACKEND_COLLECTION, DATABASE
        klass.collection_name = klass.__name__

        if DATABASE:
            if BACKEND_COLLECTION:
                this_collection = BACKEND_COLLECTION(DATABASE, klass)
                ret_obj = this_collection.find_one(*args, **kwargs)

                return ret_obj

    @classmethod
    @gen.engine
    def find_one_async(klass, *args, **kwargs):
        from Mojo.ServerHelpers.RunServer import BACKEND_COLLECTION, DATABASE
        klass.collection_name = klass.__name__

        cb = kwargs['callback']
        del(kwargs['callback'])

        if DATABASE:
            if BACKEND_COLLECTION:
                this_collection = BACKEND_COLLECTION(DATABASE, klass)
                ret_obj = yield gen.Task(this_collection.find_one, *args, **kwargs)

                cb(ret_obj)

    def __repr__(self):
        ret_str = "%s" % str(type(self.__get_value()))
        return str(ret_str)

    def __str__(self):
        return str(self.__get_value())

    def __unicode__(self):
        return unicode(self.__get_value())




class EmbeddedModelField(Field):
    """
    EmbeddedField type for models that will enable embedding of documents into the model representation.
    """
    base_type = Model

    def __init__(self, to, **kwargs):
        """
        Set the 'to' field to the model that is being embedded
        """
        self.to = to

        super(EmbeddedModelField, self).__init__(**kwargs)

    def get_value(self):
        """
        Models return a dict, so we just need to call the same function
        """
        if self.value:
            return self.value.get_value()
        else:
            return None

    def __str__(self):
        return str(self.get_value())

    __repr__ = __str__

class msgs(Model):
    _id = StringField()
    msg = StringField()
