import djcelery
import socket

from django.conf import global_settings

from functions import rel_path


########
#Imports
########
try:
    from local_settings import *

except ImportError:
    from remote_settings import *


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
CELERY_RESULT_DBURI = DATABASES['default']


########
#Storage
########
INSTALLED_APPS += (
    'storages',
    )

DEFAULT_FILE_STORAGE = 'storages.backends.s3boto.S3BotoStorage'
STATICFILES_STORAGE = 'canada.storage.CachedS3BotoStorage'
AWS_ACCESS_KEY_ID = 'AKIAILXZMFP6SQJQC7XQ'
AWS_SECRET_ACCESS_KEY = '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'
AWS_STORAGE_BUCKET_NAME = 'canadanewyork'
AWS_PRELOAD_METADATA = True #Disable to load new static file's
STATIC_URL = 'https://s3.amazonaws.com/canadanewyork/'
STATIC_ROOT = rel_path('../static')
MEDAIA_ROOT = rel_path('../media')


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
    ('canada', rel_path('static/canada')),
   )

STATICFILES_FINDERS = (
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
    )

MEDIA_URL = '/media/'

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


########
#Security
########
SECURE_FRAME_DENY = True
SECURE_HSTS_SECONDS = 1
SESSION_COOKIE_HTTPONLY = True
USE_I18N = False
SECRET_KEY = '*itk&52%kmo)f0+ase$uvsy6cmz04c@xr#7$n+bn7_=3wv0lz4'
INTERNAL_IPS = '127.0.0.1'
if 'django.middleware.csrf.CsrfViewMiddleware' not in global_settings.MIDDLEWARE_CLASSES:
    global_settings.MIDDLEWARE_CLASSES += ('django.middleware.csrf.CsrfViewMiddleware',)
global_settings.TEMPLATE_CONTEXT_PROCESSORS += ('django.core.context_processors.csrf',)

########
#Production
#######
#Cache
if 'django.middleware.cache.UpdateCacheMiddleware' not in global_settings.MIDDLEWARE_CLASSES:
    global_settings.MIDDLEWARE_CLASSES = ('django.middleware.cache.UpdateCacheMiddleware',) + global_settings.MIDDLEWARE_CLASSES
if 'django.middleware.cache.FetchFromCacheMiddleware' not in global_settings.MIDDLEWARE_CLASSES:
    global_settings.MIDDLEWARE_CLASSES += ('django.middleware.cache.FetchFromCacheMiddleware',)

INSTALLED_APPS += (
    'gunicorn',
    'compressor',
    )
CACHE_MIDDLEWARE_KEY_PREFIX = ''
CACHE_MIDDLEWARE_SECONDS = 600

COMPRESS_ROOT = STATIC_ROOT
COMPRESS_URL = STATIC_URL
COMPRESS_STORAGE = STATICFILES_STORAGE
COMPRESS_PARSER = 'compressor.parser.Html5LibParser'
COMPRESS_OFFLINE = False
COMPRESS_PRECOMPILERS = (
    ('text/x-scss', 'sass --scss {infile} {outfile}'),
)
COMPRESS_OUTPUT_DIR = 'caches_compress'

STATICFILES_FINDERS += ('compressor.finders.CompressorFinder',)

########
#Debug
########

LOCAL_DEBUG = True
GLOBAL_DEBUG = True

DEBUG = False
if (GLOBAL_DEBUG and socket.gethostname() != 'Sauls-Macbook.local')  or (LOCAL_DEBUG and socket.gethostname() == 'Sauls-Macbook.local'):
    DEBUG = True
    INSTALLED_APPS += (
        'django_extensions',
        'debug_toolbar',
        )
    if 'debug_toolbar.middleware.DebugToolbarMiddleware' not in global_settings.MIDDLEWARE_CLASSES:
        global_settings.MIDDLEWARE_CLASSES += ('debug_toolbar.middleware.DebugToolbarMiddleware',)
    global_settings.TEMPLATE_CONTEXT_PROCESSORS += ('django.core.context_processors.request',)
TEMPLATE_DEBUG = DEBUG
