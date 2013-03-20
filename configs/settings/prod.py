from .common import *


############
# SECURITY #
############
SECURE_FRAME_DENY = True
MIDDLEWARE_CLASSES += ('django.middleware.csrf.CsrfViewMiddleware',)

ALLOWED_HOSTS = (
    "{HEROKU_APP_NAME}.herokuapp.com".format(
        HEROKU_APP_NAME=os.environ.get('heroku_app_name'),
    ),
)


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
        'BACKEND': 'configs.cache_backends.JohnnyPyLibMCCache',
        'LOCATION': os.environ.get('MEMCACHIER_SERVERS'),
        'BINARY': True,
    }
}

SESSION_ENGINE = "django.contrib.sessions.backends.signed_cookies"
MESSAGE_STORAGE = "django.contrib.messages.storage.cookie.CookieStorage"
THUMBNAIL_KVSTORE = 'sorl.thumbnail.kvstores.redis_kvstore.KVStore'

###########
# LOGGING #
###########
INSTALLED_APPS = INSTALLED_APPS + (
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
            'handlers': ['sentry'],
            'propagate': False,
        },
        'raven': {
            'level': 'DEBUG',
            'handlers': ['sentry'],
            'propagate': False,
        },
        'sentry.errors': {
            'level': 'DEBUG',
            'handlers': ['sentry'],
            'propagate': False,
        },
    },
}


MIDDLEWARE_CLASSES += (
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

AWS_HEADERS = {
    "Cache-Control": "public, max-age=86400",
}

AWS_S3_FILE_OVERWRITE = False
AWS_QUERYSTRING_AUTH = False
AWS_S3_SECURE_URLS = False
AWS_REDUCED_REDUNDANCY = False
AWS_IS_GZIPPED = False


DEFAULT_FILE_STORAGE = 's3_folder_storage.s3.DefaultStorage'
STATICFILES_STORAGE = COMPRESS_STORAGE = 's3_folder_storage.s3.StaticStorage'

# Use by s3_folder_storage to save the static and other media to a path on the
# bucket
DEFAULT_S3_PATH = "media"
STATIC_S3_PATH = "static"

STATIC_ROOT = '/{}/'.format(STATIC_S3_PATH)
STATIC_URL = 'http://{}/{}/'.format(AWS_STORAGE_BUCKET_NAME, STATIC_S3_PATH)

ADMIN_MEDIA_PREFIX = STATIC_URL + 'admin/'
