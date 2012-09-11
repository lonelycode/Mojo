from tornado.web import RequestHandler
from Mojo.Auth.models import User, Session
from Mojo.Auth.SessionManager import SessionManager
from tornado import gen
import logging

class SessionMixin_Sync(RequestHandler):
    @property
    def session(self):
        if hasattr(self, '_session') is False:
            self._session = SessionManager(self)
        return self._session


    def _check_has_session_attr(self):
        if hasattr(self, 'session') is False:
            self._session = SessionManager(self)

    def set_session_key(self, key, value):
        if self.session.session_model is None:
            self.get_session_object()

        self.session._set_session_key(key, value)
        self.save_session_object()

    def get_session_key(self, key, default=None):
        if self.session.session_model is None:
            self.get_session_object()

        value = self.session._get_session_key(key)
        if value:
            return value
        else:
            return default

    def create_new_session(self):
        new_session_model = self.session._create_new_session()
        self.session.session_model = new_session_model
        self.save_session_object()

    def save_session_object(self):
        if self.session.session_model is not None:
            self.session.session_model.save()
        else:
            self.create_new_session()

    def get_session_object(self):
        thisSessionObject = Session.find_one({'session_key':self.session.session_id})
        if thisSessionObject is not None:
            self.session.session_model = thisSessionObject

        return thisSessionObject


    def get_user_from_db(self, uid=None, username=None):
        if self.application.mojo_settings.USE_AUTH:
            req = {}
            if uid:
                req['_id'] = uid
            if username:
                req[username] = username

            thisUser = User.find_one(req)
            return thisUser
        else:
            logging.warning('Mojo Auth module not implemented, to use this function please implement Mojo.Auth')

class SessionMixin_Async(RequestHandler):
    @property
    def session(self):
        if hasattr(self, '_session') is False:
            self._session = SessionManager(self)
        return self._session


    def _check_has_session_attr(self):
        if hasattr(self, 'session') is False:
            self._session = SessionManager(self)

    @gen.engine
    def set_session_key(self, key, value):
        if self.session.session_model is None:
            yield gen.Task(self.get_session_object)

        self.session._set_session_key(key, value)
        self.save_session_object()

    @gen.engine
    def get_session_key(self, key, callback, default=None):
        if self.session.session_model is None:
            yield gen.Task(self.get_session_object)

        value = self.session._get_session_key(key)
        if value:
            callback(value)
        else:
            callback(default)

    def create_new_session(self):
        new_session_model = self.session._create_new_session()
        self.session.session_model = new_session_model
        self.save_session_object()

    @gen.engine
    def save_session_object(self):
        if self.session.session_model is not None:
            yield gen.Task(self.session.session_model.save_async)
        else:
            self.create_new_session()

    @gen.engine
    def get_session_object(self, callback):
        thisSessionObject = yield gen.Task(Session.find_one_async, {'session_key':self.session.session_id})

        if thisSessionObject is not None:
            self.session.session_model = thisSessionObject
        else:
            self.create_new_session()

        callback(thisSessionObject)


    def get_user_from_db(self, uid=None, username=None):
        if self.application.mojo_settings.USE_AUTH:
            req = {}
            if uid:
                req['_id'] = uid
            if username:
                req[username] = username

            thisUser = User.find_one(req)
            return thisUser
        else:
            logging.warning('Mojo Auth module not implemented, to use this function please implement Mojo.Auth')