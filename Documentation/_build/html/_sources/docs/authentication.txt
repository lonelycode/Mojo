Using Mojo's Auth and Session Mixins
====================================

To make Tornado a bit easier to use and integrate with your application, Mojo provides a sesison management mixin that
adds database-backed sessions to your requests.

The Session Mixin assumes that a database backend and ORM is present, which is why it comes in both sync and async flavors.
The AuthMixin does not assume that a database is present and solely uses the set_cookie functionality of Tornado to make
the get_current_user functionality work.

AuthMixin
---------

The AuthMixin basically overrides get_current_user() in the MojoRequestHandler and adds a SessionManager object to the
attributes of the RequestHandler. Using the SessionManager, it is possible to login/logout the user::

    if thisUser is not None:
        if is_authenticated:
            SessionManager(request)._login(thisUser) #Will make the relevant changes to the cookies.
            return True
        else:
            return False
    else:
        return False

Using it in a request might look like::

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

The SessionMixin
----------------

The SessionMixin comes in two flavours: Syncronous and Asyncronous, depending on what backend is being used in Mojo.
To implement the SessionMixin, simply add it to the inheritance list as part of your RequestManager::

    from Mojo.Auth.Mixins.SessionMixins import SessionMixin_Sync
    class loginHandler(MojoRequestHandler, SessionMixin_Sync):

                def get(self):
                    pass

The SessionMixin exposes some basic functionality that will let you get and set session data as part of your site and save
it to the database.

All session data is stored in the SessionModel as a Base64 encoded string that is a ``dict``. To get and set session
values is quite straightforward::

    from Mojo.Auth.Mixins.SessionMixins import SessionMixin_Sync
        class loginHandler(MojoRequestHandler, SessionMixin_Sync):

                def get(self):
                    self.set_session_key('keyname', 'value')

                    value = self.get_session_key('keyname')

                    self.render('template.html', session_key_value = value)

