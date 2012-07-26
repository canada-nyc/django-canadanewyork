#!/usr/bin/env python
import os

from fabric import api

from django.db.models.loading import AppCache


@api.task(alias='run')
def run_local(debug=False):
    if debug:
        api.local('python manage.py runserver_plus')
    api.local('foreman start -e .env_local')


def reload_modules():
    cache = AppCache()

    curdir = os.getcwd()

    for app in cache.get_apps():
        f = app.__file__
        if f.startswith(curdir) and f.endswith('.pyc'):
            os.remove(f)
        __import__(app.__name__)
        reload(app)

    from django.utils.datastructures import SortedDict
    cache.app_store = SortedDict()
    cache.app_models = SortedDict()
    cache.app_errors = {}
    cache.handled = {}
    cache.loaded = False
