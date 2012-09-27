Mojo Views
==========

Mojo views are where you will write most of your application and page handling logic. In the ``views.py`` file, you will
sub-clas the MojoRequestHandler class to create your application.

The MojoRequestHandler is a slightly modified version of the basic Tornado RequestHandler that makes the local templates available to
the interpreter and adds support for prettier error formatting, it is also required to make the ``SessionMixin`` and ``AuthMixin``
classes to work as they depend on the ``MojoRequestHandler`` base class.

*Note:* It completely possible to develop with Mojo using standard ``equestHandlers``, simply subclass them as you would normally
and use them in your ``urls.py``

Views Quick-start:
------------------

To write your first view, subclas the MojoRequestHandler class, type thi into your view handler::

    from Mojo.RequestHandlers.MojoHandler import MojoRequestHandler

    class HelloWorldHandler(MojoRequestHandler):
        def get(self, *args, **kwargs):
            self.render('hello.html')

And then mak sure it is accessible in your ``urls.py`` file::

    from views import *

    urlpatterns = [
        #Place your URL Routes / RequestHandler mappings in here for this app, e.g.
        ('/',      HelloWorldHandler),
    ]

You will also need to actually create the template file, ``hello.html``, it could lok somwthing like this::

    <!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN"
            "http://www.w3.org/TR/html4/loose.dtd">
    <html>
    <head>
        <title>Hello from Mojo!</title>
    </head>
    <body>
        <h1>Hi there, I'm a template inside Mojo!</h1>
        <p>This is a tempalte file that is stored in your apps template directory.</p>
    </body>
    </html>

Save this file to your app ``templates`` directory and make sure that your app is listed in the ``settings.py`` ``INSTALLED_APPS``
 setting::

    INSTALLED_APPS = [
         'HelloWorldApp',
    ]

Now you just need to run your server, in a command line window, in your project directory type::

    python runserver.py

If your server is already running, and you have ``DEBUG=True`` set in your ``settings.py`` file, it should automatically restart when you save
the above changes.

When you navigate to ``http://localhost:8000/`` you should see your template being rendered out...

The MojoRequestHandler behaves the same way as the Tornado request handler, we recommend the reader check the Tornado documentation
to get fully up to speed with what the capabilities are of ``RequestHandler`` objects.
