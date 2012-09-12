Mojo.Backends
=============

Mojo abstracts the database interaction away from the object mapper through the use of a backend. These backends offer a
'safe' interface for the model prototype to use to access base functions of the driver (such as ``save``, ``find``, ``find_one`` etc.).

The back-ends essentially treanslate the input parameters down to the base driver. Currently Mojo ships with two backends:
one for ``Pymongo`` and the other for ``Asyncmongo``.

Part of the reason for developing Mojo was to be able to easily decide what style of driver to use without having to rewrite
many functions (or at least with only minor changes), as the asynchronous style of writing is so different from traditional
development while retaining data integrity in your schemas.

Mojo supports both blocking and non-blocking drivers to ensure that both styles of development can be harnessed without
forcing the developer down a specific path.

It is easy to add new back-ends by subclassing the ``Mojo.Backends.base_interface`` and referencing it in your settings file.

..  automodule:: Mojo.Backends.base_interface
    :members:

Included Backends
-----------------

Currently Mojo ships with two backends:

- ``Pymongo`` (blocking)
- ``Asyncmongo`` (non-blocking)

Using Backends
~~~~~~~~~~~~~~

To use a backend in your project, make sure you have the driver installed
using pip or setup tools first, and then add the following to your ``settings.py`` file::

    DATABASE = {
        'backend': 'Mojo.Backends.<BACKEND-MODULE>.<BACKEND>',
        'is_async': False,
        'name': 'test',
        'host': '127.0.0.1',
        'port': 27017
    }

for example, to use the asyncmongo
back-end::

    DATABASE = {
        'backend': 'Mojo.Backends.AsyncmongoBackend.asyncmongo_backend',
        'is_async': False,
        'name': 'test',
        'host': '127.0.0.1',
        'port': 27017
    }

Any models you implement will use the appropriate driver, just make sure you are calling the ``_async`` functions instead of
the regular ones if you are using a non-blocking driver!

Asyncmongo
~~~~~~~~~~

The Asyncmongo backend is written around the asyncmongo driver developed by bit.ly and is closely designed around Pymongo.

Using the Asyncmongo back end is similar to any asynchronous task in Tornado development::

    class thisHandler(MojoRequestHandler, MojoAuthMixin, SessionMixin_Async):

        @tornado.web.asynchronous
        @gen.engine
        def get(self):

            this_user = yield gen.Task(Users.find_one_async,{'username':'martin'})

            if this_user:
                print 'Returned user: ', this_user.username

            self.render('template.html', this_user=this_user)

The back end exposes the base functions as listed above (``find``, ``find_one``, ``save``, ``insert``, ``delete``) and
can then be accessed via the model objects as described in the ``Auth.ObjectMapper.ModelPrototype``, which exposes the
asyncmongo driver functions as <function_name>_async() instead of the direct association.

PyMongo
~~~~~~~

The pymongo backend is written around the driver written by the creators of MongoDB, usage is sraightforward enough::

    class thisHandler(MojoRequestHandler, MojoAuthMixin, SessionMixin_Async):

            def get(self):

                this_user = Users.find_one({'username':'martin'})

                if this_user:
                    print 'Returned user: ', this_user.username

                self.render('template.html', this_user=this_user)


The back end exposes the base functions as listed above (``find``, ``find_one``, ``save``, ``insert``, ``delete``) and
can then be accessed via the model objects as described in the ``Auth.ObjectMapper.ModelPrototype``, which exposes the
pymongo driver functions.