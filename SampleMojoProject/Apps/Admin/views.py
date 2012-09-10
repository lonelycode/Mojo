import tornado.web
from tornado import gen
from Mojo.RequestHandlers.MojoHandler import MojoRequestHandler
from Mojo.Auth.AuthManager import authenticate, login, set_password
from Mojo.Auth.models import User, Session
from Mojo.Auth.SessionManager import SessionManager, Setup_session, Reset_session
import logging

class loginHandler(MojoRequestHandler):
    @tornado.web.asynchronous
    @gen.engine
    def get(self):

        if self.get_current_user() is not None:
            self.redirect('/admin/')
        else:
            self.render('login.html', error=None)

    @tornado.web.asynchronous
    @gen.engine
    def post(self):

        username = self.get_argument('username')
        password = self.get_argument('password')

        # DBFUNCTION: Let's check the user out
        thisUser = User.find_one({'username':username})

        logging.debug('Found user: %s' % thisUser)

        if thisUser is not None:
            # We now have a user, let's authenticate her
            is_authenticated = authenticate(thisUser, password)
            logging.debug('Checking is user is authenticated: %s' % str(is_authenticated))
            if is_authenticated:
                # Now for session mojo
                sm = SessionManager(self)
                # Get a session ID or creae a new session object
                session, created = sm.get_or_create_session()
                if created:
                    # We have created a new session object, let's assign it to our Session Manager
                    sm.session_model = session
                    logging.debug('Created new session key: %s' %  sm.session_model.session_key)
                else:
                    # DBFUNCTION: We have a session ID, let's grab it from the Database
                    logging.debug('Found session key %s in cookie, retrieving from DB' % session)
                    this_session = self.get_session_object(session)

                    #If we find a session in the DB, let's reset it's date and time expiry
                    if this_session != None:
                        logging.debug('Session found in database, setting up existing session')
                        this_session = Reset_session(this_session)
                        #Then let's put it in our session manager
                        sm.session_model = this_session
                    else:
                        # Session wasn't in the Db, so let's create a new session model and reassign the session key
                        logging.debug("Session ID wasn't in database, creating new")
                        sm.session_model = Setup_session(Session())
                        sm.session_model.session_key = session

                #User is authenticated, and has a session, let's log them in!
                sm._log_user_in(thisUser)

                # DBFUNCTION: Login means sweet FA if it's not in the DB, so let's save that
                self.save_session_object(sm)

                self.redirect('/admin/')
            else:
                self.render('login.html', error='Login failed')
        else:
            self.render('login.html', error='Login failed')


class logoutHandler(MojoRequestHandler):
    @tornado.web.asynchronous
    @gen.engine
    def get(self):
        # Set up a session manager and load in the request
        sm = SessionManager(self)
        # Create a new session object or get a session ID
        session, created = sm.get_or_create_session()

        print 'Created: ', created
        print 'session: ', session

        if not created:
            # DBFUNCTION: Session exists, let's grab it from the DB
            sessionmodel = self.get_session_object(session)
            print 'Retrieved from DB:', sessionmodel
            # Assign it to the session manager
            sm.session_model = sessionmodel
            # Log the user out (in the session)
            sm._logout()
            print 'Logged out.'
            print 'Check: ', sm._is_logged_in()

            # DBFUNCTION: Save the session object to the DB for the nxt time they log in
            self.save_session_object(sm)

        self.render('logout.html', message='Your face')

class adminHomeHandler(MojoRequestHandler):
    @tornado.web.asynchronous
    @gen.engine
    def get(self):

        self.render('main.html', message='Your face')

class modelActionHandler(MojoRequestHandler):
    @tornado.web.asynchronous
    @gen.engine
    def get(self):

        self.render('main.html', message='Your face')