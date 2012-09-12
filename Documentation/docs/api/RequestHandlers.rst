Mojo.RequestHandlers
====================

The ``MojoRequestHandler`` is the basic ``RequestHandler`` class that you use in your application instead of the standard
Tornado ``RequestHandler``::

    class pageHandler(MojoRequestHandler, MojoAuthMixin, SessionMixin_Sync):
    #You don't need to use the Mixins, but they make life a lot easier.

        def get(self):
            #Do some cool stuff

            self.render('login.html', error=None)

..  automodule:: Mojo.RequestHandlers.MojoHandler
    :members:
