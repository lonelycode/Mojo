Mojo.SocketHandlers
===================

Mojo has added some simple convenience to TornadIO2 SocketConnections by adding two key dictionaries to the framework.
These dictionaries are populated (and depopulated) as users connect to the site.

The dictionaries that are made available are:

- CURRENT_SESSIONS: Keyed by the session ID of the user
- LOGGED_IN_SESSIONS: Keyed by the user ID of the (logged in) user (requires Mojo.Auth to be enabled).

**Usage:** ::

    from Mojo.SocketHandlers.BaseSocketHandler import MojoSocketHandler, CURRENT_SESSIONS, LOGGED_IN_SESSIONS

    #Setup your socket connections here (remember to subclass MojoSocketHandler)
    class SocketConnectionHandler(MojoSocketHandler):
        def on_message(self, msg):
            pass

..  automodule:: Mojo.SocketHandlers.BaseSocketHandler
    :members: