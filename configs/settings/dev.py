from .common import *


#########
# LOCAL #
#########
INTERNAL_IPS = ('127.0.0.1',)


###########
# STORAGE #
###########
MEDIA_ROOT = rel_path('tmp/media/')
STATIC_ROOT = rel_path('tmp/static/')

'''
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': rel_path('tmp/sqlite.db'),
        'USER': '',
        'PASSWORD': '',
        'HOST': '',
        'PORT': '',
    }
}
'''

#########
# DEBUG #
#########
DEBUG = TEMPLATE_DEBUG = True

INSTALLED_APPS += ('debug_toolbar',)
MIDDLEWARE_CLASSES += ('debug_toolbar.middleware.DebugToolbarMiddleware',)
DEBUG_TOOLBAR_CONFIG = {
    'INTERCEPT_REDIRECTS': False,
}

# https://github.com/tomchristie/django-pdb
INSTALLED_APPS += ('django_pdb',)
MIDDLEWARE_CLASSES += ('django_pdb.middleware.PdbMiddleware',)
