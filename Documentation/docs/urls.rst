Routing pages with URL's
========================

Mojo moves the URL definition of your app to the file ``urls.py``, this file contains a list object called ``url_patterns``
that contains tuples mapping a URL to a ``RequestHandler`` in your ``views.py``.

All entries work the same way as they do with standard Tornado mappings, when your server starts up, Mojo will automatically
concatenate all the URL's for you into a single pattern set to ensure that all your apps are available in the project
without mixing functionality across apps::

    from views import myRequestHandler

    urlpatterns = [
        ('/hello', myRequestHandler),
        ]

All URL patterns can be regex groups - see the Tornado documentation for more details on how to use the URL routing
in a Tornado app.