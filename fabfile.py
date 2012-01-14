#!/usr/bin/env python
from __future__ import with_statement

import os.path
import xmlrpclib
import pip

from fabric.api import local, settings
from fabric.contrib.console import confirm


def run(celery=False):
    local('python canada/manage.py runserver_plus')
    if celery:
        with settings(warn_only=True):
            local('tab "label rabbitmq;sudo rabbitmq-server"')
        local('tab "c;label celerycam;python canada/manage.py celerycam"')
        local('tab "c;label celeryWorker;python canada/manage.py celeryd -E -l INFO"')
def sass():
    local('label sass;sass --watch canada/static/sass:canada/static/css')


def shell():
    local('python canada/manage.py shell')


APPS_TO_WATCH = ['artists', 'exhibitions', 'updates', 'bulkmail', 'press', 'search', 'frontpage']
def sync():
    local('python canada/manage.py syncdb')
    with settings(warn_only=True):
        for app in APPS_TO_WATCH:
            if os.path.isfile(os.path.abspath(os.path.join(os.path.dirname(__file__), "canada", app, 'migrations/0001_initial.py'))):
                local('python canada/manage.py schemamigration %s --auto' % app)
            else:
                local('python canada/manage.py schemamigration %s --initial' % app)

        local('python canada/manage.py migrate')
        update()


def upload():
    local('cd canada;gondor deploy primary master')


def sr():
    sync()
    run()


def update():
    print 'Checking for updates:'
    ignore = [
        'PIL',
        ]
    print 'Ignoring:'
    for i in ignore:
        print '    {}'.format(i)
    pypi = xmlrpclib.ServerProxy('http://pypi.python.org/pypi')
    cant_find = []
    updates = {}
    for dist in pip.get_installed_distributions():
        print 'Checking {}...'.format(dist.project_name)
        if not dist.project_name in ignore:
            available = pypi.package_releases(dist.project_name)
            if not available:
                # Try to capitalize pkg name
                available = pypi.package_releases(dist.project_name.capitalize())
            if not available:
                cant_find.append(dist)
            elif available[0] != dist.version:
                updates[dist.project_name] = available[0]
    for dist in updates:
        print '{:17}-> {}'.format(dist, updates[dist])
    if not updates:
        print 'No Updates'
    for dist in cant_find:
        print '{:20} Cant Find'.format(dist)
    if updates and confirm("Install all updates?"):
            #req_original = open(os.path.abspath(os.path.join(os.path.dirname(__file__), str("requirements.txt")))).readlines()
            for dist in updates:
                local('pip install --upgrade {}'.format(dist))
                #for l_number, line in enumerate(req_original):
                #    if line.startswith(dist) or line.startswith(dist.lower()):
                #        print 'Replacing {} with {} in requirements.txt'.format(line, '{}=={}'.format(dist, updates[dist]))
                #        req_original[l_number] = '{}=={}'.format(dist, updates[dist])
