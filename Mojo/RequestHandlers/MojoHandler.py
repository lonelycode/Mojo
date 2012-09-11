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

    def get_template_path(self):
        return self.module_template_path