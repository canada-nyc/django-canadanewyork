import os

from memcacheify import memcacheify
import dj_database_url

from .common import *

DEBUG = True
TEMPLATE_DEBUG = DEBUG

########
#Cache
########

CACHES = memcacheify()  # http://rdegges.github.com/django-heroku-memcacheify/
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
#Storage
########
INSTALLED_APPS += ('storages',)
DEFAULT_FILE_STORAGE = 'storages.backends.s3boto.S3BotoStorage'
AWS_ACCESS_KEY_ID = environ['AWS_ACCESS_KEY_ID']
AWS_SECRET_ACCESS_KEY = environ['AWS_SECRET_ACCESS_KEY']
AWS_STORAGE_BUCKET_NAME = 'canadanewyork'
STATICFILES_STORAGE = DEFAULT_FILE_STORAGE

#Compress
COMPRESS_STORAGE = STATICFILES_STORAGE
COMPRESS_URL = 'https://{}.s3.amazonaws.com/'.format(AWS_STORAGE_BUCKET_NAME)


########
#Queue
########
RQ_QUEUES = {
    'default': {
        'URL': os.getenv('REDISTOGO_URL'),
        'DB': 0,
    },
}


########
#Security
########
SECURE_FRAME_DENY = True
