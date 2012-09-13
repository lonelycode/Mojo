# Managed request handler that will also
# specify app-level template directories
# as part of it's init procedure.

from tornado.web import RequestHandler
import datetime, logging, os
from tornado import gen
from Mojo.RequestHandlers.PrettyOutputMixin import UncaughtExceptionMixin

from Mojo.Auth.models import Session, User

class MojoRequestHandler(RequestHandler, UncaughtExceptionMixin):
    """
    The ``MojoRequestHandler`` is the starting point of any request in Mojo, subclass this for every URL
    you want to serve in Mojo.

    The ``MojoRequestHandler`` has some handy properties:

    - ``application``: This is a reference to the server object, and give access to project settings
    - ``application.mojo_settings``: All variables declared in your ``settings.py`` file
    - ``db``: the database Session object (for direct access to the DB you can get to the driver through ``db._db.<function>``)

    If you are using the ``MojoAuthMixin`` or ``SessionMixin``, the request handlers expand with many more management functions to make life
    easier for the developer.
    """
    def __init__(self, application, request, **kwargs):

        #TODO: This is really hacky, must be a more elegant wy to build up the path name
        thisModule = __import__(self.__module__)
        mods = self.__module__.split('.')
        thisAppName = mods[mods.index('Apps') +1]
        template_path = 'Apps/%s/templates/' % (thisAppName)

        self.module_template_path = template_path
        self.application = application


        RequestHandler.__init__(self, application, request,**kwargs)

    def get_template_path(self):
        return self.module_template_path