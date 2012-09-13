from Mojo.RequestHandlers.MojoHandler import MojoRequestHandler


class myRequestHandler(MojoRequestHandler):
    def get(self):

        self.render('test.html', message='Your face')