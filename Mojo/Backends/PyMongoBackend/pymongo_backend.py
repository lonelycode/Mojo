from Mojo.Backends.base_interface import CollectionModelInterface, SessionInterface
import pymongo
import logging

class Session(SessionInterface):
    def _setup_connection(self):
        self._db = pymongo.Connection(
            host=self.host,
            port=self.port,
        )[self.db_name]

class Collection(CollectionModelInterface):
    def find_one(self, *args, **kwargs):
        return_dict = self.session._db[self.collection_name].find_one(*args, **kwargs)
        return self._return_model_object(return_dict)

    def find(self, *args, **kwargs):
        return_cursor = self.session._db[self.collection_name].find(*args, **kwargs)
        return_model_list = [self._return_model_object(i) for i in return_cursor]
        return return_model_list

    def insert(self, documents, *args, **kwargs):
        ret_vals = []
        if type(documents) != list:
            raise ValueError("Insert requires a list as input, for single query use [document]")
        else:
            insert_list = []
            for doc in documents:
                del doc['_id']
                insert_list.append(doc.get_value())

            ids = self.session._db[self.collection_name].insert(insert_list)

            index = 0
            for doc in documents:
                doc['_id'] = ids[index]
                index += 1

                ret_vals.append(doc)

            return ret_vals

    def save(self, document, *args, **kwargs):
        temp_doc = dict(document)

        if not document._id:
            del temp_doc['_id']

        returnID = self.session._db[self.collection_name].save(temp_doc, *args, **kwargs)
        document._id = returnID
        return document

    def delete(self, documents, *args, **kwargs):
        return_values = []
        for document in documents:
            ret_val = self.session._db[self.collection_name].remove(document._id)
            return_values.append(ret_val)

        return return_values