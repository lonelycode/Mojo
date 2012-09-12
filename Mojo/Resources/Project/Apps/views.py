import tornado.web
from Mojo.RequestHandlers.MojoHandler import MojoRequestHandler

#Set up your request handlers here

class NewInstallHandler(MojoRequestHandler):
    def get(self, *args, **kwargs):
        self.render('mojo.html')