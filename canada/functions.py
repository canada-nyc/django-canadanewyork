import os
from django.db.models.loading import AppCache


def add_to_middleware(MIDDLEWARE_CLASSES, middleware, prepend=False):
    if middleware not in MIDDLEWARE_CLASSES:
        if prepend:
            return (middleware,) + MIDDLEWARE_CLASSES
        else:
            return MIDDLEWARE_CLASSES + (middleware,)
    else:
        return MIDDLEWARE_CLASSES


def reload_modules():
    cache = AppCache()
    cwd = os.getcwd()

    for app in cache.get_apps():
        if cwd in app.__file__:
            os.remove(app.__file__)
        __import__(app.__name__)
        reload(app)

    from django.utils.datastructures import SortedDict
    cache.app_store = SortedDict()
    cache.app_models = SortedDict()
    cache.app_errors = {}
    cache.handled = {}
    cache.loaded = False
