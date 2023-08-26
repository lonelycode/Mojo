Mojo Apps
=========

When developing with Mojo, it's more elegant to modularise functionality into Apps, and this is the default behaviour
of the Mojo server loader.

Apps serve as a collection of RequestHandlers, URL Mappings, Models and Templates that make up a set of functionality
in your project.

To get started with an app in your project, you can use the ``mojo_manager.py`` helper application that will auto create
your project folder for you::

    python mojo_manager.py -a [YOUR_APP_NAME]

This will create an app folder with certain key files:

- ``models.py``: This is where you define your models which can be used with your database and forms
- ``socket_handlers.py``: This is where you define your SocketIO behaviour, each app has it's own dedicated (multiplexed) channel under ``/[appname]Socket`` to separate out functionality
- ``ui_modules.py``: The ui_modules you might or might not be using
- ``urls.py``: The URL mappings for your request handlers
- ``views.py``: A list of your ``RequestHandler`` classes that handle your app functionality

