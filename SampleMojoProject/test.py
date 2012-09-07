from Mojo.RequestHandlers.MojoHandler import createRequestHandler
from tornado.web import RequestHandler

myClass = createRequestHandler()

class myRequestHandler(createRequestHandler()):
    def get(self):
        render('test.html', {})