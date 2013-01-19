from .common import *


############
# SECURITY #
############
SECURE_FRAME_DENY = True
MIDDLEWARE_CLASSES += ('django.middleware.csrf.CsrfViewMiddleware',)


###########
# Caching #
###########
MIDDLEWARE_CLASSES += (
    'django.middleware.gzip.GZipMiddleware',
)

TEMPLATE_LOADERS = (
    ('django.template.loaders.cached.Loader', (
        'django.template.loaders.filesystem.Loader',
        'django.template.loaders.app_directories.Loader',
    )),
)

CACHES = {
    'default': {
        'BACKEND': 'django_pylibmc.memcached.PyLibMCCache',
        #'LOCATION': os.environ.get('MEMCACHIER_SERVERS'),
        #'TIMEOUT': 500,
        #'BINARY': True,
    }
}

MIDDLEWARE_CLASSES += ('django.middleware.cache.FetchFromCacheMiddleware',)
# Must be first
MIDDLEWARE_CLASSES = ('django.middleware.cache.UpdateCacheMiddleware',) + MIDDLEWARE_CLASSES


###########
# LOGGING #
###########
RAVEN_CONFIG = {
    'dsn': os.environ.get('SENTRY_DSN'),
}

RQ_SENTRY_DSN = RAVEN_CONFIG['dns']

INSTALLED_APPS = (
    'raven.contrib.django.raven_compat',
)

LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'root': {
        'level': 'WARNING',
        'handlers': ['sentry'],
    },
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s'
        },
    },
    'handlers': {
        'sentry': {
            'level': 'ERROR',
            'class': 'raven.contrib.django.raven_compat.handlers.SentryHandler',
        },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose'
        }
    },
    'loggers': {
        'django.db.backends': {
            'level': 'ERROR',
            'handlers': ['console'],
            'propagate': False,
        },
        'raven': {
            'level': 'DEBUG',
            'handlers': ['console'],
            'propagate': False,
        },
        'sentry.errors': {
            'level': 'DEBUG',
            'handlers': ['console'],
            'propagate': False,
        },
    },
}

MIDDLEWARE_CLASSES = MIDDLEWARE_CLASSES + (
    'raven.contrib.django.raven_compat.middleware.SentryResponseErrorIdMiddleware',
)

###########
# STORAGE #
###########
INSTALLED_APPS += (
    'storages',
    's3_folder_storage',
)
AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY')
AWS_STORAGE_BUCKET_NAME = AWS_S3_CUSTOM_DOMAIN = os.environ.get('AWS_BUCKET')

# Faster sync
AWS_PRELOAD_METADATA = True
# Hopefully prettier urls?
AWS_QUERYSTRING_AUTH = False


AWS_S3_SECURE_URLS = False

DEFAULT_FILE_STORAGE = THUMBNAIL_DEFAULT_STORAGE = 's3_folder_storage.s3.DefaultStorage'
STATICFILES_STORAGE = COMPRESS_STORAGE = 's3_folder_storage.s3.StaticStorage'

# Use by s3_folder_storage to save the static and other media to a path on the
# bucket
STATIC_S3_PATH = "static"
DEFAULT_S3_PATH = "media"

STATIC_ROOT = '/{}/'.format(STATIC_S3_PATH)
STATIC_URL = 'http://{}/{}/'.format(AWS_STORAGE_BUCKET_NAME, STATIC_S3_PATH)

ADMIN_MEDIA_PREFIX = STATIC_URL + 'admin/'
