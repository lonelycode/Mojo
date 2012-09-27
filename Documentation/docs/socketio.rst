Mojo and SocketIO
=================

One of the strengths of Tornado is it's ability to handle asynchronous requests and support for websockets. Top make Mojo
more of a responsive framework, we've decided to bundle ``TornadIO2`` functionality as part of the overall package.

For those that do not know what ``TornadIO2`` is, it is a ``SocketIO`` server implementation written in Python for Tornado, and
makes it transparent to implement SocketIO clients into your app.

By default, Mojo will start a ``TornadIO`` server for you that multiplexes a channel connection for each of the apps in your
project.

So if you have 2 apps: ``App1`` and ``App2``, then you will be able to speak to either of these apps via SocketIO on the
client by connecting to the ``/App1Socket`` or ``/App2Socket`` channels in your client side configuration.

To configure what commands the server should intitiate on connection, send event or receive event, simply edit the ``socket_handlers.py``
file in your app folder::

    from Mojo.SocketHandlers.BaseSocketHandler import MojoSocketHandler, CURRENT_SESSIONS, LOGGED_IN_SESSIONS

    #Setup your socket connections here
    class SocketConnectionHandler(MojoSocketHandler):

        def on_message(self, msg):
            #Do something cool when a message arrives
            pass

To make the most of ``TornadIO2`` and ``SocketIO`` we'd recommend you read the documentation for both as their inner workings fall outside
of the remit of the Mojo documentation.

Helpful Tracking
----------------

Mojo does some handy tracking for you if you use the ``MojoSocketHandler`` to manage your socket connections. Mojo will
automatically register all connections in two variables that enable you to communicate with users directly from the start,
these variables are ``CURRENT_SESSIONS`` and ``LOGGED_IN_SESSIONS``

``CURRENT_SESSIONS``
^^^^^^^^^^^^^^^^^^^^

This is a dictionary object that will track each connection by their Session ID. The session ID is a secure Tornado cookie
that is called ``session_id``, if you are using the ``MojoSessionMixin`` module, this will be set for you, however if you
want to roll your own session management, you can just set this cookie and the user will be tracked by the ID in the ``SocketHandler``.

This will enable you to do something like::

    from Mojo.RequestHandlers.MojoHandler import MojoRequestHandler
    from Mojo.SocketHandlers.BaseSocketHandler import CURRENT_SESSIONS
    import json

        class HelloWorldHandler(MojoRequestHandler):
            def get(self, *args, **kwargs):

                jsonObj = json.dumps({'data':'%s has joined the chat' % (self.session_id)})

                for session in CURRENT_SESSIONS:
                    session.emit('joinedStatus', jsonObj)

                self.render('hello.html')

Although the above code is not functional, the principle is valid - in this example, you could use the CURRENT_SESSIONS object
to broadcast to all active users that a new user has joined the conversation.

``LOGGED_IN_SESSIONS``
^^^^^^^^^^^^^^^^^^^^^^

If you are using the AuthMixin from Mojo, then it will set an encrypted cookie of the name ``logged_in`` with the user ID
of the current user. Naturally, you can set this yourself to whatever identifier you like if you decide not use the mixins.

Any session that is identified as Logged in will be added to the ``LOGGED_IN_SESSIONS`` dictionary, and will enable you to
interact with users. In a similar vein to the ``CURRENT_SESSIONS`` object, you would now be able to send specific messages only
to logged in members of your app.