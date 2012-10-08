.. Mojo documentation master file, created by
   sphinx-quickstart on Fri Sep  7 14:39:41 2012.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Mojo v0.1.2 - a framework for Tornado
=====================================

Mojo is a framework that makes it easy and quick to build Tornado projects that scale.

**Some key features of Mojo:**

- A lightweight and flexible ORM that makes developing easy
- ORM is based off a 'backend' system, enabling you to write your own backend and extend the ORM to other databases without altering your code
- Authentication and session mixins so you don't need to roll-your-own implementation or third parties
- Integration with wtForms, with the ability to use your Models as Forms and to populate models from Form data
- Modular structure so you can add functionality to your project on an app by app basis
- Prettier debugging output
- SocketIO support baked in with TornadIO2
- Project and app-creation templates that make it easy to set up new projects

The project is heavily influenced by Django, developers familiar with django will find some of the conventions in Mojo
very familiar.

To get acquainted with Mojo and get started, see the quick-start guide.

Contents:
---------

.. toctree::
    :maxdepth: 2

    docs/quickstart.rst
    docs/apps.rst
    docs/views.rst
    docs/urls.rst
    docs/models.rst
    docs/socketio.rst
    docs/authentication.rst

The Mojo API:
-------------

.. toctree::
    :maxdepth: 2

    docs/api/Auth.rst
    docs/api/Backends.rst
    docs/api/ObjectMapper.rst
    docs/api/Forms.rst
    docs/api/RequestHandlers.rst
    docs/api/SocketHandlers.rst

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

