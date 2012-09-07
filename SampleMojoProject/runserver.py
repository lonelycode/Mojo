import sys
from Mojo.ServerHelpers import RunServer

modname = globals()['__name__']
thisModule = sys.modules[modname]

RunServer.init_run_server(thisModule)