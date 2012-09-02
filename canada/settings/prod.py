from os import environ

from memcacheify import memcacheify
import dj_database_url

from .common import *

DEBUG = False
TEMPLATE_DEBUG = DEBUG

########
#Cache
########

CACHES = memcacheify()  # http://rdegges.github.com/django-heroku-memcacheify/
# Run heroku addons:add memcachier:25 for free 25m
MIDDLEWARE_CLASSES = ('django.middleware.gzip.GZipMiddleware',) + MIDDLEWARE_CLASSES

########
#Database
########
DATABASES = {'default': dj_database_url.config(default='postgres://localhost')}

########
#Server
########
INSTALLED_APPS += ('gunicorn',)
INTERNAL_IPS = ('0.0.0.0',)

########
#Email
########
EMAIL_HOST = "smtp.gmail.com"
EMAIL_PORT = 587
EMAIL_HOST_USER = "saul.shanabrook@gmail.com"
EMAIL_HOST_PASSWORD = environ.get('EMAIL_HOST_PASSWORD', '')
EMAIL_USE_TLS = True

########
#Storage
########
INSTALLED_APPS += ('storages',)
DEFAULT_FILE_STORAGE = 'storages.backends.s3boto.S3BotoStorage'
AWS_ACCESS_KEY_ID = environ['AWS_ACCESS_KEY_ID']
AWS_SECRET_ACCESS_KEY = environ['AWS_SECRET_ACCESS_KEY']
AWS_STORAGE_BUCKET_NAME = 'canadanewyork'
STATICFILES_STORAGE = DEFAULT_FILE_STORAGE

########
#Background Tasks
########
RQ = True

########
#Security
########
SECURE_FRAME_DENY = True
TEMPLATE_CONTEXT_PROCESSORS += ('django.core.context_processors.csrf',)
CSRF_COOKIE_DOMAIN = '.herokuapp.com'
