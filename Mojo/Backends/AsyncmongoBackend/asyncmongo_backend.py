from Mojo.Backends.base_interface import CollectionModelInterface, SessionInterface
import asyncmongo
from tornado import gen
import logging, copy

class Session(SessionInterface):
    def _setup_connection(self):
        self._db = asyncmongo.Client(
            pool_id='mydb',
            maxcached=10,
            maxconnections=50,
            host=self.host,
            port=self.port,
            dbname=self.db_name
        )

class Collection(CollectionModelInterface):

    @gen.engine
    def find_one(self, *args, **kwargs):

        cb = kwargs['callback']
        del(kwargs['callback'])

        return_dict = yield gen.Task(self.session._db[self.collection_name].find_one,*args, **kwargs)

        cb(self._return_model_object(return_dict[0][0]))


    @gen.engine
    def find(self, *args, **kwargs):
        cb = kwargs['callback']
        del(kwargs['callback'])

        return_cursor = yield gen.Task(self.session._db[self.collection_name].find, *args, **kwargs)
        ret_list = return_cursor[0][0]

        return_model_list = [self._return_model_object(i) for i in ret_list]

        cb(return_model_list)

    @gen.engine
    def insert(self, documents, *args, **kwargs):

        cb = kwargs['callback']
        del(kwargs['callback'])

        if type(documents) != list:
            raise ValueError("Insert requires a list as input, for single query use [document]")
        else:
            clean_docs = []
            for doc in documents:
                del doc['_id']
                clean_docs.append(doc.get_value())

            ids = yield gen.Task(self.session._db[self.collection_name].insert, clean_docs)

            cb(ids)

    @gen.engine
    def save(self, document, callback):
        temp_doc = dict(document.get_value())

        if '_id' in temp_doc.keys():
            if temp_doc['_id'] is None:
                del(temp_doc['_id'])
                logging.debug('Removed null _id value for save')
                return_tuple, error = yield gen.Task(self.session._db[self.collection_name].save, temp_doc)
            else:
                del(temp_doc['_id'])
                return_tuple, error = yield gen.Task(self.session._db[self.collection_name].update, {'_id': document._id}, {"$set":temp_doc})


#        logging.info('Asyncmongo does not return ObjectID on insert, please update _id property of model manually before further manipulation')
#        else:
#            for k, v in temp_doc.iteritems():
#                if v is None:
#                    del(temp_doc, k)
#            logging.info('Asyncmongo does not return ObjectID on insert, please update _id property of model manually before further manipulation')
#            return_tuple, error = yield gen.Task(self.session._db[self.collection_name].insert, temp_doc)

        callback(document)

    @gen.engine
    def delete(self, documents, callback):
        return_values = []
        for document in documents:
            ret_val = yield gen.Task(self.session._db[self.collection_name].remove, document._id)
            return_values.append(ret_val)

        callback(return_values)