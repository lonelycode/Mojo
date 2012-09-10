__author__ = 'buhrm'

DEBUG=True

LOG_LEVEL = 'debug'
LISTEN_PORT = 8000
SOCKET_IO_PORT = 8001
USE_XHEADERS = True

PROJECT_NAME = ''
STATIC_PATH = '/Users/buhrm/src/DynaMojoEnv/SampleMojoProject/static'

DATABASE = {
    'backend': 'Mojo.Backends.PyMongoBackend.pymongo_backend',
    'is_async': False,
    'name': 'test',
    'host': '127.0.0.1',
    'port': 27017
}

USE_AUTH = True
COOKIE_SECRET = '123456789123456789'

INSTALLED_APPS = [
    'SampleApp',
    'Admin'
]

