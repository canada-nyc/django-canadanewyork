from settings.base import *

DEBUG = True

DATABASES = {
    'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME':  rel_path('../sqlite.db'),
            'USER': '',
            'PASSWORD': '',
            'HOST': '',
            'PORT': '',
            }
    }

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
    }
}
