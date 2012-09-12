Mojo.Auth
=========

The Mojo.Auth modules are designed to make authentication easier in Tornado by providing a model framework, password
management, encryption and validation tools.

To accompany the authentication tools, there is also a session management system that makes maintaining persistent
sessions easy across requests.

This module also provides a set of Mixins that integrate the authentication and session management functionality and integrate
with either the synchronous or asynchronous mongo drivers, see the mixins section to see how this is accomplished.

AuthManager
-----------

..  automodule:: Mojo.Auth.AuthManager
    :members:

Helpers
-------

..  automodule:: Mojo.Auth.Helpers
    :members:

Auth Models
-----------

..  automodule:: Mojo.Auth.models
    :members:

Session Manager
---------------

..  automodule:: Mojo.Auth.SessionManager
    :members:
    :private-members:

Mojo.Auth.Mixins
----------------

Mixin Modules to help with Authentication and Session management

..  toctree::

    Mixins.rst
