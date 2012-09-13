#!/usr/bin/env python

import optparse
import os, sys
import shutil

import Mojo

project_files = [
    '__init__.py',
    'settings.py',
    'runserver.py',
    'Apps/__init__.py'
]

project_dirs = [
    'Apps',
    'static'
]

app_files = [
    '__init__.py',
    'socket_handlers.py',
    'ui_modules.py',
    'urls.py',
    'views.py'
]

app_dirs = [
    'templates',
    'templates/UI_modules'
]

def make_project_structure(project_name):
    print 'Creating new Mojo project: %s...' % project_name
    mojo_project_dir = os.path.dirname(Mojo.__file__) + '/Resources/Project/'
    new_project_dir = os.getcwd() + '/%s/' % project_name

    os.mkdir(new_project_dir)

    for d in project_dirs:
        os.mkdir(new_project_dir + '%s/' % d)

    for f in project_files:
        shutil.copyfile(''.join([mojo_project_dir, f]), ''.join([new_project_dir, f]))


def make_app_structure(app_name):
    print 'Creating new Mojo app: %s...' % app_name
    mojo_project_dir = os.path.dirname(Mojo.__file__) + '/Resources/Project/Apps/'
    first_template = mojo_project_dir + 'templates/mojo.html'
    new_app_dir = os.getcwd() + '/Apps/%s/' % app_name

    os.mkdir(new_app_dir)

    for d in app_dirs:
        os.mkdir(new_app_dir + '%s/' % d)

    for f in app_files:
        shutil.copyfile(''.join([mojo_project_dir, f]), ''.join([new_app_dir, f]))


    first_template_new_dir = new_app_dir + 'templates/mojo.html'
    shutil.copyfile(first_template, first_template_new_dir)


def main():
    p = optparse.OptionParser()
    p.add_option('--project', '-p', default='')
    p.add_option('--app', '-a', default='')
    options, arguments = p.parse_args()

    if options.project:
        make_project_structure(options.project)
    if options.app:
        make_app_structure(options.app)

if __name__ == '__main__':
    main()