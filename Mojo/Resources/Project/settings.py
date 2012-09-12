#This is your settings file, set up your project from here before running the server

#Set this to false to set the Tornado server up as production
DEBUG=True

#Set the verdosity of the output here, options are info,debug,warning,critical
LOG_LEVEL = 'debug'

#Set the port that the Tornado server should listen on
LISTEN_PORT = 8000

#Set the port the TornadIO2 server should listen on
SOCKET_IO_PORT = 8001

#Use XHR Headers (default True)
USE_XHEADERS = True

#Give your project a name
PROJECT_NAME = ''

#Full path to your static files directory
STATIC_PATH = '/Users/buhrm/src/DynaMojoEnv/SampleMojoProject/static'

#Enter your database information, backend options are PyMongoBackend.pymongo_backend or AsyncmongoBackend.asyncmongo_backend
DATABASE = {
    'backend': 'Mojo.Backends.PyMongoBackend.pymongo_backend',
    'name': 'test',
    'host': '127.0.0.1',
    'port': 27017
}

#Set to false if you do not want Mojo to handle your Auth functions (required for Session and Auth mixins)
USE_AUTH = True

#Login URL that authenticated pages should redirect to
LOGIN_URL = '/admin/login/'

#Your cookie secret value: CHANGE THIS AS SOON AS POSSIBLE
COOKIE_SECRET = '123456789123456789'


INSTALLED_APPS = [
    #Enter your installed apps here, e.g.:
    # 'MojoBlog',
]

