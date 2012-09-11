import tornado.web
from tornado import gen
from Mojo.RequestHandlers.MojoHandler import MojoRequestHandler
from Mojo.Auth.AuthManager import authenticate
from Mojo.Auth.models import User
from Mojo.Auth.Mixins.MojoAuthMixin import MojoAuthMixin
from Mojo.Auth.Mixins.SessionMixins import SessionMixin_Sync, SessionMixin_Async
from Mojo.Auth.SessionManager import SessionManager, Setup_session, Reset_session

import logging

class loginHandler(MojoRequestHandler, MojoAuthMixin):

    def get(self):

        if self.current_user:
            self.render('login.html', error='ALREADY LOGGED IN')
        else:
            self.render('login.html', error=None)

    @tornado.web.asynchronous
    @gen.engine
    def post(self):
        username = self.get_argument('username')
        password = self.get_argument('password')

        target = self.get_argument('next', '/admin/')

        # DBFUNCTION: Let's check the user out
        thisUser = yield gen.Task(User.find_one,{'username':username})

        logging.debug('Found user: %s' % thisUser)

        if thisUser is not None:
            # We now have a user, let's authenticate her
            is_authenticated = authenticate(thisUser, password)
            logging.debug('Checking is user is authenticated: %s' % str(is_authenticated))
            if is_authenticated:
                # Now for session mojo
                if hasattr(self, 'session'):
                    self.session._login(thisUser)
                else:
                    SessionManager(self)._login(thisUser)

                self.redirect(target)
            else:
                self.render('login.html', error='Login failed')
        else:
            self.render('login.html', error='Login failed')


class logoutHandler(MojoRequestHandler, MojoAuthMixin):
    def get(self):

        if hasattr(self, 'session'):
            self.session._logout()
        else:
            SessionManager(self)._logout()

        self.render('logout.html', message='Your face')

class adminHomeHandler(MojoRequestHandler, MojoAuthMixin):

    @tornado.web.authenticated
    def get(self):

        print 'Current User:', self.current_user

        self.render('main.html', message='Your face')

class modelActionHandler(MojoRequestHandler):
    @tornado.web.authenticated
    def get(self):

        self.render('main.html', message='Your face')