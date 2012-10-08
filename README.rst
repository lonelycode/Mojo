Mojo v0.1.1 - a framework for Tornado
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

*Mojo documentation is available courtesy of ReadTheDocs: http://mojo.readthedocs.org/, all documentation is written
in Sphinx.*

Quickstart: Using Mojo for the first time
=========================================

This is a quick-start tutorial that will get you set up and running with Mojo for the first time.

Installation
------------

1. Download the Mojo distribution: https://raw.github.com/lonelycode/Mojo/master/dist/Mojo-0.1.tar.gz
2. Decompress the zip file
3. Make sure you have installed the required support packages: ``Tornado``, ``TornadIO2``, ``bcrypt`` and ``wtforms``
4. From the command line in the new folder run ``python setup.py install``

This should install Mojo into your python path. However, there is one more step that you may need to do to fully
take advantage of Mojo's helper apps, and that is to make ``mojo_manager`` available in your ``PATH``, for linux and Mac OSX users,
this can be accomplished by doing something like::

    ln /usr/bin/python2.7/Lib/site-packages/Mojo/mojo_manager.py /usr/sbin/mojo_manager.py
    chmod +x /usr/sbin/mojo_manager.py

On windows, adding the Mojo site-packages directory should be enough to give gloabl access to ``mojo_manager``

Once you've done that, you should be able to test your installation by opeining a python window and typing::

    import Mojo

If there are no import errors then you shoulod be ready to get started.

*Note:* It is recommended to deploy Mojo in something like virtualenv to ensure you can easily keep it (and your app)
up to date without affecting your main Python setup and other projects.

Your first project
------------------

Mojo sets up it's projects as a project folder that contains a series of Apps, these apps are independent from one another
and offer a way to group different functional areas of your app away into discrete units. The typical Mojo project will have a
folder structure that looks like::

    --[ProjectName]
    ----[static]
    ----[Apps]
    ------[App 1]
    --------[templates]
    --------models.py
    --------ui_modules.py
    --------urls.py
    --------views.py
    ------[App 2]
    ------[App 3]
    ----settings.py
    ----runserver.py

A quick run down of what each of these files and folders are:

* ``[ProjectName]``: Your projct folder, this houses all the apps, modules settings and server for your tornado project
* ``[static]``: All your static assets can be placed in here and they will be referenced automatically when you use the ``static_url("images/logo.png")`` built in tornado function
* ``[Apps]``: Houses all of your individual apps, these break down into a series of base files that make your app work:

  * ``[App 1]/models.py``: This is your model definition file, here you set out what database tables you want to use
  * ``[App 1]/ui_modules.py``: Your UI Modules for Tornado are housed here, these are automatically loaded so they can be used directly from your templates
  * ``[App 1]/urls.py``: The URL's for this app, ampping to the relevant Request Handlers
  * ``[App 1]/views.py``: The request handlers that will manage the various app's functions

* ``settings.py``: All the settings for your application
* ``runserver.py``: This, strangely enough, runs your web server

To create your first app, you simply need to invok ethe mojo_manager application,
this will create your project folder as follows::

    > mojo_manager.py -p MyNewProject
    > cd MyNewProject
    > mojo_manager.py -a HelloWorldApp

That's it, all the files you need to get started should be created and in nbamed appropriately.

Setup the App
-------------

To get started, lets set up your settings.py to get your first server up and running. Open ``settings.py`` in your favourite editor
and make sure the ``INSTALLED_APPS`` section looks like this::

    INSTALLED_APPS = [
        'HelloWorldApp',
    ]

Once you've made the change, simply save the file and open up your terminal window in the directory where ``runserver.py`` is located, then
type the following::

    python runserver.py

You should see::

    Starting Mojo tornado server.
    DEBUG:root:Setting up url routers:
    DEBUG:root:--Added URL's for: blog_app
    DEBUG:root:--Adding UI Modules for blog_app
    DEBUG:root:--Added SocketHandler for: blog_app
    DEBUG:root:Found DATABASE setting - creating session for DB: mojo_blog
    INFO:root:Starting up tornadio server on port '8001'
    INFO:root:Entering IOLoop...

If you navigate to ``http://localhost:8000`` you should see the Mojo welcome page. *Congratulations, you are running Mojo!*