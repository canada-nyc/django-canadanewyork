from os import path, environ

from django.conf.global_settings import *

import canada


SITE_ROOT = path.dirname(path.realpath(canada.__file__))

########
#CANADA
########
CANADA_IMAGE_SIZE = 'x300'
CANADA_FRONTPAGE_IMAGE_SIZE = 'x400'
CANADA_ADMIN_THUMBS_SIZE = 'x60'

INSTALLED_APPS = (
    'canada.apps.artists',
    'canada.apps.exhibitions',
    'canada.apps.press',
    'canada.apps.updates',
    'canada.apps.bulkmail',
    'canada.apps.updates',
    'canada.apps.frontpage',
    'canada.apps.info',
    'canada.apps.base'
  )

TEMPLATE_CONTEXT_PROCESSORS += ('canada.context_processors.image_size',)

########
#External Packages
########
INSTALLED_APPS += (
    'south',
    'grappelli',
    'sorl.thumbnail',
    'smart_selects',
    'storages',
    'bootstrapform',
  )

GRAPPELLI_ADMIN_TITLE = 'CANADA'


########
#Django
########
INSTALLED_APPS += (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.admin',
    'django.contrib.staticfiles',
    'django.contrib.markup',
    'django.contrib.sites',
  )

SITE_ID = 1
SECRET_KEY = environ['SECRET_KEY']
WSGI_APPLICATION = 'manage.application'

#Static/Media
STATICFILES_DIRS = (
    ('canada', path.join(SITE_ROOT, 'static')),
  )

MEDIA_URL = '/media/'
MEDIA_ROOT = path.normpath(path.join(SITE_ROOT, '../media/'))

STATIC_URL = '/static/'
STATIC_ROOT = path.normpath(path.join(SITE_ROOT, '../static/'))

FIXTURE_DIRS = (path.join(SITE_ROOT, 'fixtures'),)

#Admin
LOGIN_URL = '/admin/'
ADMIN_MEDIA_PREFIX = STATIC_URL + "grappelli/"
ADMINS = (
    ('Saul Shanabrook', 'saul.shanabrook@gmail.com'),
  )


#Urls
ROOT_URLCONF = 'canada.urls'
APPEND_SLASH = True

#Templates
TEMPLATE_DIRS = (
    path.join(SITE_ROOT, 'templates'),
  )

DATE_FORMAT = 'F j, Y'
