

class SessionInterface(object):
    def __init__(self, host='127.0.0.1', port=27017, db_name = None):
        self.host = host
        self.port = port
        self.db_name = db_name

        self._db = None

        self._setup_connection()

    def _setup_connection(self):
        pass

class CollectionModelInterface(object):
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
        pass

    def find_one(self, *args, **kwargs):
        pass

    def save(self, document, *args, **kwargs):
        pass

    def delete(self, documents, *args, **kwargs):
        pass

    def insert(self, documents, *args, **kwargs):
        pass

