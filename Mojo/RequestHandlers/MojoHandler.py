# Managed request handler that will also
# specify app-level template directories
# as part of it's init procedure.

from tornado.web import RequestHandler
import datetime, logging, os
from tornado import gen

from Mojo.Auth.models import Session, User

#TODO:
#For login, logout functionality - use a combination of get and set session object and the auth helpers
#Login procedure would be:
#- Post to login URL
#- Login handler will:
#-- Get username, password
#-- Lookup userObj from DB
#-- Check pw against user object
#-- pass / fail
#-- get or create session
#-- set logged in session key
#-- save session
#-- redirect

#Logout procedure would be:
#-- GET to logout URI
#-- Get Session Object from DB
#-- if not created - set logged in to false
#-- save session
#-- otherwise - do nothing
#-- redirect

class MojoRequestHandler(RequestHandler):
    def __init__(self, application, request, **kwargs):

        #TODO: This is really hacky, must be a more elegant wy to build up the path name
        thisModule = __import__(self.__module__)
        mods = self.__module__.split('.')
        thisAppName = mods[mods.index('Apps') +1]
        template_path = '%s/Apps/%s/templates/' % (os.path.dirname(thisModule.__file__), thisAppName)

        self.module_template_path = template_path
        self.application = application


        RequestHandler.__init__(self, application, request,**kwargs)


    def get_current_user(self):
        #TODO: Factor this out into a seperate Mixin (then ywe can implement async and sync)?
        if self.application.mojo_settings.USE_AUTH:

            logging.debug('get_current_user called, not cached!')
            from Mojo.Auth.SessionManager import SessionManager
            from bson.objectid import ObjectId

            SM = SessionManager(self)
            s_cookie, created = SM.get_or_create_session()

            if created:
                logging.debug('Session is created... no user to report')
                return None
            else:
                logging.debug('Found a valid session object.')
                #We have a valid session - get the session details from the DB and store in SM
                this_session = self.get_session_object(s_cookie)

                if this_session is not None:
                    logging.debug('Found session in DB, setting up')
                    SM.session_model = this_session
                else:
                    #Bollocks, the session isn't in the database! Return None
                    logging.debug("Couldn't find the session in the DB: %s" % str(s_cookie))
                    return None

                if SM._is_session_valid():
                    #Is the session valid? If so:
                    logging.debug('Session is still valid.')

                    uid = SM._is_logged_in()

                    if uid is not False:
                        logging.debug('User is logged in, UID: %s' % str(uid))
                        #if is_logged_in -> get User from DB object and return
                        this_user = User.find_one({'_id':ObjectId(uid)})

                        if this_user is not None:
                            return this_user
                        else:
                            return None
                    else:
                        return None
                else:
                    return None

        else:
            logging.warning('Mojo Auth module not implemented, please override get_current_user or implement Auth module.')

    def save_session_object(self, session_manager):
        # TODO: Factor out to a mixin to implement async and sync diff
        if self.application.mojo_settings.USE_AUTH:
            if session_manager.session_model != None:
                session_manager.session_model.save()
        else:
            logging.warning('Mojo Auth module not implemented, to use Sessions please implement Mojo.Auth')

    def get_session_object(self, session_id):
        # TODO: Factor out to a mixin to implement async and sync diff
        if self.application.mojo_settings.USE_AUTH:
            return Session.find_one({'session_key':session_id})
        else:
            logging.warning('Mojo Auth module not implemented, to use Sessions please implement Mojo.Auth')

    def get_template_path(self):
        return self.module_template_path