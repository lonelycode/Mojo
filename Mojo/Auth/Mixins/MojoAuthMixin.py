from tornado.web import RequestHandler
import logging

class MojoAuthMixin(RequestHandler):
    """
    The Auth mixin will make the get_current_user functionality available that takes advantage of the Mojo.Auth familly
    of modules and models.

    **Example Usage:** ::

        import tornado.web
        from Mojo.RequestHandlers.MojoHandler import MojoRequestHandler
        from Mojo.Auth.Mixins.MojoAuthMixin import MojoAuthMixin
        from Mojo.Auth.models import User
        from Mojo.Auth.Helpers import login_assistant

        #To implement the mixin, simply subclass it alongside the regular MojoRequestHandler and the authentication
        #funcitonality will be come available.

        class loginHandler(MojoRequestHandler, MojoAuthMixin):

            def get(self):
                #Override the get function to render the page, check current_user to see if we're already logged in
                if self.current_user:
                    self.render('login.html', error='ALREADY LOGGED IN')
                else:
                    self.render('login.html', error=None)

            def post(self):
                #Get the username and password from the request
                username = self.get_argument('username')
                password = self.get_argument('password')

                target = self.get_argument('next', '/admin/')

                #Get the user from the database
                thisUser = User.find_one({'username':username})

                #Log the user in using the login assistant
                if login_assistant(thisUser, password, self):
                    self.redirect(target)
                else:
                    self.render('login.html', error='Login failed')

    """
    def get_current_user(self):
        """
        Overrides ``get_current_user`` to return the ``logged_in`` value from the sesison cookies. This function uses the
        ``SessionManager`` class to get and set cookies (this is to ensure that Mojo-specific functionality and keys are consistent).
        """
        if self.application.mojo_settings.USE_AUTH:

            logging.debug('get_current_user called, not cached!')
            from Mojo.Auth.SessionManager import SessionManager

            if hasattr(self, 'session'):
                SM = self.session
            else:
                SM = SessionManager(self)
                self.session = SM

            if not SM._is_logged_in():
                logging.debug('Session is created... no user to report')
                return None
            else:
                return SM.cookies['logged_in']

        else:
            logging.warning('Mojo Auth module not implemented, please override get_current_user or implement Auth module.')