import djcelery

from django.conf.global_settings import *
import datetime

from functions import rel_path, add_to_middleware


########
#CANADA
########
CANADA_SLIDER_IMAGE_SIZE = 'x300'
CANADA_FRONTPAGE_IMAGE_SIZE = 'x400'
CANADA_UPDATES_IMAGE_SIZE = 'x400'
INSTALLED_APPS = (
    'canada.artists',
    'canada.exhibitions',
    'canada.press',
    'canada.updates',
    'canada.bulkmail',
    'canada.updates',
    'canada.search',
    'canada.frontpage',
  )


########
#Packages
########
INSTALLED_APPS += (
    'south',
    'grappelli',
    'sorl.thumbnail',
  )

GRAPPELLI_ADMIN_TITLE = 'CANADA'


########
#Celery/Email
########
djcelery.setup_loader()

INSTALLED_APPS += (
    'djcelery',
    'djcelery_email',
    'celery',
    'djkombu',
  )

EMAIL_HOST = "smtp.gmail.com"
EMAIL_PORT = 587
EMAIL_HOST_USER = "saul.shanabrook@gmail.com"
EMAIL_HOST_PASSWORD = "3j}s^52G-qH69%kY"
EMAIL_USE_TLS = True
EMAIL_BACKEND = 'djcelery_email.backends.CeleryEmailBackend'

BROKER_BACKEND = "djkombu.transport.DatabaseTransport"



########
#Django
########
SITE_ID = 1
DEBUG = False

INSTALLED_APPS += (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.flatpages',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.admin',
    'django.contrib.staticfiles',
    'django.contrib.markup',
  )

#Static/Media
STATICFILES_DIRS = (
    ('canada', rel_path('static')),
  )

MEDIA_URL = '/media/'

STATIC_URL = '/static/'
STATIC_ROOT = rel_path('../static')
MEDAIA_ROOT = rel_path('../media')


#Admin
LOGIN_URL = '/admin/'
ADMIN_MEDIA_PREFIX = STATIC_URL + "grappelli/"
ADMINS = (
    ('Saul Shanabrook', 'saul.shanabrook@gmail.com'),
  )


#Urls
ROOT_URLCONF = 'canada.urls'

#Templates
TEMPLATE_DIRS = (
    rel_path('templates'),
  )

MIDDLEWARE_CLASSES = add_to_middleware(MIDDLEWARE_CLASSES, 'django.middleware.gzip.GZipMiddleware', prepend=True)


########
#Cache
########

MIDDLEWARE_CLASSES = add_to_middleware(MIDDLEWARE_CLASSES, 'django.middleware.cache.UpdateCacheMiddleware', prepend=True)
MIDDLEWARE_CLASSES = add_to_middleware(MIDDLEWARE_CLASSES, 'django.middleware.cache.FetchFromCacheMiddleware')

CACHE_MIDDLEWARE_KEY_PREFIX = ''
CACHE_MIDDLEWARE_SECONDS = 600


########
#Security
########
SECURE_FRAME_DENY = True
SECURE_HSTS_SECONDS = 1
SESSION_COOKIE_HTTPONLY = True
USE_I18N = False
SECRET_KEY = '*itk&52%kmo)f0+ase$uvsy6cmz04c@xr#7$n+bn7_=3wv0lz4'
INTERNAL_IPS = '127.0.0.1'

TEMPLATE_CONTEXT_PROCESSORS += ('django.core.context_processors.csrf',)
