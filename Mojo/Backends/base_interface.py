

class SessionInterface(object):
    """
    Session wrapper around the database connection, takes host, port and database
    information to enable the database session.

    If your database has a specific style of connecting, subclass this class and override the
    ``_setup_connection`` function to connect to make the connection available to your backend.

    Back-ends access the Session through a ``session._db`` property that is assigned during the server boot up::

        #Snippet from the Pymongo backend

        def find_one(self, *args, **kwargs):
            return_dict = self.session._db[self.collection_name].find_one(*args, **kwargs)
            return self._return_model_object(return_dict)

    """
    def __init__(self, host='127.0.0.1', port=27017, db_name = None):
        self.host = host
        self.port = port
        self.db_name = db_name

        self._db = None

        self._setup_connection()

    def _setup_connection(self):
        """
        Override this function to enable the connection as part of the server boot.
        """
        pass

class CollectionModelInterface(object):
    """
    The CollectionModelInterface exposes the basic functions of the driver to the ModelPrototype, it will
    expect to have these functions *at least* in order to be fully functional:

    - ``find``
    - ``find_one``
    - ``save``
    - ``delete``

    To create your own back-end, subclass this class and override all the functions with the relevant access functions
    and parameter styles.

    Mojo tends to use Pymongo style dictionary access, it is recommended to try to adhere to this format.

    """
    def __init__(self, session, model):
        self.session = session
        self.model = model
        if type(self.model) == type:
            self.collection_name = self.model.__name__
        else:
            self.collection_name = type(self.model).__name__

    def _return_model_object(self,dict):
        if dict:
            return self.model(dict)
        else:
            return None

    def find(self, *args, **kwargs):
        """
        Override this to enable ``find`` in the database
        """
        pass

    def find_one(self, *args, **kwargs):
        """
        Override this to enable ``find-one`` in the database
        """
        pass

    def save(self, document, *args, **kwargs):
        """
        Override this to enable ``save`` in the database
        """
        pass

    def delete(self, documents, *args, **kwargs):
        """
        Override this to enable ``delete`` in the database
        """
        pass

    def insert(self, documents, *args, **kwargs):
        """
        Override this to enable ``insert`` in the database
        """
        pass

