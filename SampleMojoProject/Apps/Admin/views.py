import tornado.web
from tornado import gen
from Mojo.RequestHandlers.MojoHandler import MojoRequestHandler
from Mojo.Auth.models import User
from Mojo.Auth.Mixins.MojoAuthMixin import MojoAuthMixin
from Mojo.Auth.Mixins.SessionMixins import SessionMixin_Async
from Mojo.Auth.Helpers import login_assistant, logout_assistant

class loginHandler(MojoRequestHandler, MojoAuthMixin, SessionMixin_Async):

    def test_callback(self, value):
        print 'THIS IS A CALLBACK', value

    @tornado.web.asynchronous
    @gen.engine
    def get(self):

        a = yield gen.Task(self.get_session_key,'logged_in')

        print 'YIELED STSTEMENT: ', a

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

        #DBFUNCTION: Let's check the user out
        thisUser = yield gen.Task(User.find_one,{'username':username})

        if login_assistant(thisUser, password, self):
            self.redirect(target)

        else:
            self.render('login.html', error='Login failed')


class logoutHandler(MojoRequestHandler, MojoAuthMixin, SessionMixin_Async):
    def get(self):

        logout_assistant(self)

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