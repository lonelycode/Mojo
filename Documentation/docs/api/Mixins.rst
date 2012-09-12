Mojo.Auth.Mixins
================

The Mojo Mixins are there to make authentication and session managemeent easy in your application without
having to load in the whole machinery in each request.

MojoAuthMixin
-------------

MojoAuthMixin is designed to override the get_current_user functionality of a standard Tornado RequestHandler to provide
straightforward and secure authentication. Makes use of the SessionManager class to manage cookies.

..  automodule:: Mojo.Auth.Mixins.MojoAuthMixin
    :members:

SessionMixins
-------------

Session mixins are designed to make persistent session management features from SessionManager available as part of your RequestHandler,
the mixins enable getting and setting of persistent session data (sessions are stored in the database) and also nifty helper functions
that wrap SessionManager.

The mixins come in two flavours: Synchronous and Asynchronous to ensure they work fully with your preferred database backend.

Synchronous (blocking) Session Mixin
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

..  autoclass:: Mojo.Auth.Mixins.SessionMixins.SessionMixin_Sync
    :members:

Asynchronous (non-blocking) Session Mixin
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

..  autoclass:: Mojo.Auth.Mixins.SessionMixins.SessionMixin_Async
    :members:

