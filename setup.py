#!/usr/bin/env python

from distutils.core import setup

setup(name='Mojo',
    version='0.1',
    description='Mojo Tornado Framework',
    author='Martin Buhr',
    author_email='martin@jive.ly',
    packages=['Mojo',
              'Mojo.Auth',
              'Mojo.Auth.Mixins',
              'Mojo.Backends',
              'Mojo.Backends.AsyncmongoBackend',
              'Mojo.Backends.PyMongoBackend',
              'Mojo.ObjectMapper',
              'Mojo.Resources',
              'Mojo.Resources.Project',
              'Mojo.Resources.Project.Apps',
              'Mojo.RequestHandlers',
              'Mojo.ServerHelpers',
              'Mojo.SocketHandlers'
              ],
    package_data={'Mojo': ['Resources/Project/Apps/templates/*.html']},
    requires=['Tornado',
              'tornadio2',
              'pymongo',
              'bson'],

)