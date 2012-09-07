# Managed request handler that will also
# specify app-level template directories
# as part of it's init procedure.

from tornado.web import RequestHandler
import datetime, logging, os
from tornado import gen

from Mojo.Auth.models import Session, User

#TODO:
#For login, logout functionality - use a combination of get and set session object and the auth helpers

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
        if self.application.mojo_settings.USE_AUTH:
            from Mojo.Auth.SessionManager import SessionManager
            from bson.objectid import ObjectId

            SM = SessionManager(self)
            s_cookie, created = SM.get_or_create_session()

            if created:
                return None
            else:
                #We have a valid session - get the session details from the DB and store in SM
                this_session = self.get_session_object(s_cookie.value)
                if this_session:
                    SM.session_model = this_session
                else:
                    #Bollocks, the session isn't in the database! Return None
                    return None

                if SM._is_session_valid():
                    #Is the session valid? If so:
                    uid = SM._is_logged_in()
                    if uid:
                        #if is_logged_in -> get User from DB object and return
                        this_user = User.find_one({'_id':ObjectId(uid)})
                        if this_user:
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
        if self.application.mojo_settings.USE_AUTH:
            if session_manager.session_model:
                session_manager.session_model.save()

        else:
            logging.warning('Mojo Auth module not implemented, to use Sessions please implement Mojo.Auth')

    def get_session_object(self, session_id):
        Session.find_one({'session_key':session_id})

    def get_template_path(self):
        return self.module_template_path