import tornado.ioloop
import tornado.web
import tornadio2
import sys, os
import tornado
import logging

from tornadio2 import SocketConnection
from Mojo.SocketHandlers.ControlConnection import ControlConnection


DATABASE = None
BACKEND_COLLECTION = ''

log_level = {
    "DEBUG":logging.DEBUG,
    "INFO":logging.INFO,
    "WARNING":logging.WARNING,
    "CRITICAL":logging.CRITICAL
    }



class DynaMojoTornadoApplication(tornado.web.Application):
    def __init__(self, PROJECT_SETTINGS, SocketRouter, ProjectRoutes, ui_modules, db_session=None):
        handlers = SocketRouter.apply_routes(ProjectRoutes)

        settings = dict(
            app_title=PROJECT_SETTINGS.PROJECT_NAME,
            autoescape=None,
            socket_io_port=PROJECT_SETTINGS.SOCKET_IO_PORT,
            debug=PROJECT_SETTINGS.DEBUG,
            xheaders=PROJECT_SETTINGS.USE_XHEADERS,
            static_path = PROJECT_SETTINGS.STATIC_PATH,
            ui_modules = ui_modules,
            cookie_secret=PROJECT_SETTINGS.COOKIE_SECRET,
            login_url = PROJECT_SETTINGS.LOGIN_URL
        )

        self.db = db_session
        self.mojo_settings = PROJECT_SETTINGS

        tornado.web.Application.__init__(self, handlers, **settings)

def get_module_name(path):
    dirs = path.split('/')
    pm_name = dirs[len(dirs)-1]

    return pm_name

def setup_socket_handler_routers(module_name, installed_apps):
    endpoints = {'/DynaMojoControl': ControlConnection}

    for appName in installed_apps:
        app_socket_handler = None
        socket_module_string = 'from %s.Apps.%s.socket_handlers import SocketConnectionHandler as app_socket_handler' % (module_name, appName)
        exec(socket_module_string)

        if app_socket_handler:
            endpoint_str = '/%sSocket' % appName
            new_endpoint = {endpoint_str:app_socket_handler}
            endpoints.update(new_endpoint)
            logging.debug("--Added SocketHandler for: %s" % (appName))
        else:
            logging.debug("--Couldn't find any Socket Handlers for app: %s" % (appName))

    # This voodoo creates the SocketConnection class dynamically
    thisSocketConnection = type(
        'SocketConnection',
        (object,),
        dict(__endpoints__ = endpoints))

    SocketRouter = tornadio2.TornadioRouter(thisSocketConnection)

    return SocketRouter

def init_run_server(ProjectModule):
    print "Starting Mojo tornado server."
    pm_path = os.path.dirname(ProjectModule.__file__) + '/'
    settings_path = pm_path + 'settings.py'
    sys.path.append(pm_path)
    sys.path.append(settings_path)

    module_name = get_module_name(os.path.dirname(ProjectModule.__file__))

    project_details_import_string = 'import %s.settings as project_settings' % (module_name)
    exec(project_details_import_string)
    logging.basicConfig(level = log_level[project_settings.LOG_LEVEL.upper()])

    logging.debug(  'Setting up url routers:')
    routes = []
    for appName in project_settings.INSTALLED_APPS:
        urls_string = 'import %s.Apps.%s.urls as urls' % (module_name, appName)
        exec(urls_string)
        routes.extend(urls.urlpatterns)
        logging.debug("--Added URL's for: %s" % (appName))

    for appName in project_settings.INSTALLED_APPS:
        logging.debug("--Adding UI Modules for %s" % appName)
        ui_module_string = 'from %s.Apps.%s import ui_modules' % (module_name, appName)
        exec(ui_module_string)

        ui_modules = ui_modules

    thisSocketRouter = setup_socket_handler_routers(module_name, project_settings.INSTALLED_APPS)

    db_session = None
    if project_settings.DATABASE:
        Session = None
        logging.debug('Found DATABASE setting - creating session for DB: %s' % project_settings.DATABASE['name'])
        backend_import_str = 'from %s import Session, Collection' % (project_settings.DATABASE['backend'])
        exec(backend_import_str)

        global DATABASE
        DATABASE = Session(host=project_settings.DATABASE['host'], port=project_settings.DATABASE['port'], db_name = project_settings.DATABASE['name'])
        global BACKEND_COLLECTION
        BACKEND_COLLECTION = Collection


    application = DynaMojoTornadoApplication(project_settings, thisSocketRouter, routes, ui_modules, db_session)

    application.listen(project_settings.LISTEN_PORT)
    tornadio2.SocketServer(application)