from tornado.web import RequestHandler
from Mojo.Auth.models import User, Session
from Mojo.Auth.SessionManager import SessionManager
from tornado import gen
from bson.objectid import ObjectId
import logging

class SessionMixin_Sync(RequestHandler):
    """
    Synchronous Session Mixin ``RequestHandler`` base class. Exposes session management functions via a ``SessionManager``
    object and ties these back using the ORM to the database, this mixin will use a blocking driver.

    **Usage:** ::

        from Mojo.Auth.Mixins.SessionMixins import SessionMixin_Sync

        class loginHandler(MojoRequestHandler, SessionMixin_Sync):
            def get(self):
                ...

    """

    @property
    def session(self):
        """
        Session property - holds a ``SessionManager`` object that is initialised with the current ``RequestHandler`` as context,
        will initialise on first access.
        """
        if hasattr(self, '_session') is False:
            self._session = SessionManager(self)
        return self._session

    def _check_has_session_attr(self):
        """
        Checks to see if there's a session attribute in the class, otherwise creates one.
        """
        if hasattr(self, 'session') is False:
            self._session = SessionManager(self)

    def set_session_key(self, key, value):
        """
        Sets a session key and saves it to the database (not a cookie - sessions are identified by a ``session_id`` in
        the secure cookie collection and for security purposes are encoded and stored in the database so as not to leak
        any information).

        **Usage:** ::

            class loginHandler(MojoRequestHandler, SessionMixin_Sync):

                def get(self):
                    self.set_session_key('test_value', 'hello world!')
                    new_value = self.get_session_key('test_value')

                    #Should render the 'test_value' session variable if it's in the template.
                    self.render('main.html', session_value=new_value)

        """
        if self.session.session_model is None:
            self.get_session_object()

        self.session._set_session_key(key, value)
        self.save_session_object()

    def get_session_key(self, key, default=None):
        """
        Gets a session key from the database based on the ``session_id`` supplied by the ``RequestHandler``. Similarly to
        ``set_session_key``, this is not a cookie value, but a persistent session variable from the database.

        **Usage:** ::

            class loginHandler(MojoRequestHandler, SessionMixin_Sync):

                def get(self):
                    this_session_value = self.get_session_key('test_value')

                    #Should render the 'test_value' session variable if it's in the template.
                    self.render('main.html', session_value=new_value)

        """

        if self.session.session_model is None:
            self.get_session_object()

        value = self.session._get_session_key(key)
        if value:
            return value
        else:
            return default

    def create_new_session(self):
        """
        Wrapper around the SessionManagers _create_new_session() method, but will save the session to DB instead of
        having to manage it manually.
        """
        new_session_model = self.session._create_new_session()
        self.session.session_model = new_session_model
        self.save_session_object()

    def save_session_object(self):
        """
        Saves the session model to the database, in this case it's a synchronous (blocking) operation. If there is no
        session to save, will create a new one (which is then saved automatically)
        """
        if self.session.session_model is not None:
            self.session.session_model.save()
        else:
            self.create_new_session()

    def get_session_object(self):
        """
        Returns the whole session_model object and assigns it to itself.
        """
        thisSessionObject = Session.find_one({'session_key':self.session.session_id})
        if thisSessionObject is not None:
            self.session.session_model = thisSessionObject
        else:
            from Mojo.Auth.SessionManager import Setup_session
            self.session.session_model = Setup_session(Session())

        return thisSessionObject


    def get_user_from_db(self, uid=None, username=None):
        """
        Gets a user from the database, this is such a common operation it offers a quick and simple way to return the full
        user object from the database either by supplying the ``username`` or ``password``.
        """
        if self.application.mojo_settings.USE_AUTH:
            req = {}
            if uid:
                req['_id'] = ObjectId(uid)
            if username:
                req[username] = username

            thisUser = User.find_one(req)
            return thisUser
        else:
            logging.warning('Mojo Auth module not implemented, to use this function please implement Mojo.Auth')

class SessionMixin_Async(RequestHandler):
    """
    Asynchronous Session Mixin ``RequestHandler`` base class. Exposes session management functions via a ``SessionManager``
    object and ties these back using the ORM to the database, this mixin will use a non-blocking driver.

    Is compatible with gen.Task or callback-style implementations, the preferred method is the gen.Task implementation.

    **Usage:** ::

        from Mojo.Auth.Mixins.SessionMixins import SessionMixin_Async

        class loginHandler(MojoRequestHandler, SessionMixin_Async):

            @tornado.web.asynchronous
            @gen.engine
            def get(self):
                ...

    """
    @property
    def session(self):
        """
        Session property - holds a ``SessionManager`` object that is initialised with the current ``RequestHandler`` as context,
        will initialise on first access.
        """
        if hasattr(self, '_session') is False:
            self._session = SessionManager(self)
        return self._session


    def _check_has_session_attr(self):
        """
        Checks to see if there's a session attribute in the class, otherwise creates one.
        """
        if hasattr(self, 'session') is False:
            self._session = SessionManager(self)

    @gen.engine
    def set_session_key(self, key, value):
        """
        Sets a session key and saves it to the database (not a cookie - sessions are identified by a ``session_id`` in
        the secure cookie collection and for security purposes are encoded and stored in the database so as not to leak
        any information).

        **Usage:** ::

            class loginHandler(MojoRequestHandler, SessionMixin_Async):

                @tornado.web.asynchronous
                @gen.engine
                def get(self):
                    yield gen.Task(self.set_session_key,'test_value', 'hello world!')

                    new_value = yield gen.Task(self.get_session_key,'test_value')

                    #Should render the 'test_value' session variable if it's in the template.
                    self.render('main.html', session_value=new_value)

        """
        if self.session.session_model is None:
            yield gen.Task(self.get_session_object)

        self.session._set_session_key(key, value)
        self.save_session_object()

    @gen.engine
    def get_session_key(self, key, callback, default=None):
        """
        Gets a session key from the database based on the ``session_id`` supplied by the ``RequestHandler``. Similarly to
        ``set_session_key``, this is not a cookie value, but a persistent session variable from the database.

        **Usage:** ::

            class loginHandler(MojoRequestHandler, SessionMixin_Sync):

                @tornado.web.asynchronous
                @gen.engine
                def get(self):
                    new_value = yield gen.Task(self.get_session_key,'test_value')

                    #Should render the 'test_value' session variable if it's in the template.
                    self.render('main.html', session_value=new_value)

        """
        if self.session.session_model is None:
            yield gen.Task(self.get_session_object)

        value = self.session._get_session_key(key)
        if value:
            callback(value)
        else:
            callback(default)

    def create_new_session(self):
        """
        Wrapper around the SessionManagers _create_new_session() method, but will save the session to DB instead of
        having to manage it manually.
        """

        new_session_model = self.session._create_new_session()
        self.session.session_model = new_session_model
        self.save_session_object()

    @gen.engine
    def save_session_object(self):
        """
        Saves the session model to the database, in this case it's an asynchronous (non-blocking) operation. If there is no
        session to save, will create a new one (which is then saved automatically)
        """
        if self.session.session_model is not None:
            yield gen.Task(self.session.session_model.save_async)
        else:
            self.create_new_session()

    @gen.engine
    def get_session_object(self, callback):
        """
        Returns the whole session_model object and assigns it to itself.
        """
        thisSessionObject = yield gen.Task(Session.find_one_async, {'session_key':self.session.session_id})

        if thisSessionObject is not None:
            self.session.session_model = thisSessionObject
        else:
            self.create_new_session()

        callback(thisSessionObject)


    def get_user_from_db(self, uid=None, username=None):
        """
        Gets a user from the database, this is such a common operation it offers a quick and simple way to return the full
        user object from the database either by supplying the ``username`` or ``password``.
        """
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