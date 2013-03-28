import os

import dj_database_url
from memcacheify import memcacheify

from django.conf.global_settings import *

from libs.common.utils import rel_path, SITE_ROOT


##################
# DJANGO DEFAULT #
##################

SECRET_KEY = os.environ.get('SECRET_KEY', '*YSHFUIH&GAHJBJCZKCY)P#R')
WSGI_APPLICATION = 'wsgi.application'
DATE_FORMAT = 'F j'
ROOT_URLCONF = 'configs.urls'
PREPEND_WWW = False

##########
# CANADA #
##########
INSTALLED_APPS = (
    'apps.artists',
    'apps.exhibitions',
    'apps.press',
    'apps.updates',
    'apps.photos',

    'libs.common',
)


##########
# MODELS #
##########
INSTALLED_APPS += (
    "url_tracker",
)
MIDDLEWARE_CLASSES += ('url_tracker.middleware.URLChangePermanentRedirectMiddleware',)


#########
# ADMIN #
#########
INSTALLED_APPS += ('grappelli',)

INSTALLED_APPS += (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.humanize',
)

GRAPPELLI_ADMIN_TITLE = 'canada'


#############
# TEMPLATES #
#############
TEMPLATE_DIRS = rel_path('templates')

INSTALLED_APPS += ('markdown_deux',)
MARKDOWN_DEUX_STYLES = {
    "default": {
        "safe_mode": "escape",
    },
}

INSTALLED_APPS += ('sekizai',)
TEMPLATE_CONTEXT_PROCESSORS += ('sekizai.context_processors.sekizai',)


##############
# THUMBNAILS #
##############
INSTALLED_APPS += ('sorl.thumbnail',)


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

CACHES = memcacheify()

SESSION_ENGINE = "django.contrib.sessions.backends.signed_cookies"
MESSAGE_STORAGE = "django.contrib.messages.storage.cookie.CookieStorage"

MIDDLEWARE_CLASSES += ('django.middleware.cache.FetchFromCacheMiddleware',)
# Must be first
MIDDLEWARE_CLASSES = ('django.middleware.cache.UpdateCacheMiddleware',) + MIDDLEWARE_CLASSES

SESSION_ENGINE = "django.contrib.sessions.backends.cached_db"


#############
# FLATPAGES #
#############
INSTALLED_APPS += ('django.contrib.flatpages',)

###########
# STORAGE #
###########
INSTALLED_APPS += ('django.contrib.staticfiles',)
STATICFILES_DIRS = (
    ('canada', rel_path('static')),
)


INSTALLED_APPS += (
    'storages',
)
AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY')
AWS_STORAGE_BUCKET_NAME = os.environ.get('AWS_BUCKET')
AWS_S3_CUSTOM_DOMAIN = AWS_STORAGE_BUCKET_NAME
AWS_HEADERS = {
    "Cache-Control": "public, max-age=31536000",
}
AWS_QUERYSTRING_AUTH = False
AWS_S3_SECURE_URLS = False
AWS_IS_GZIPPED = True
AWS_PRELOAD_METADATA = True


DEFAULT_FILE_STORAGE = 'storages.backends.s3boto.S3BotoStorage'
STATICFILES_STORAGE = DEFAULT_FILE_STORAGE

STATIC_URL = 'http://{}/'.format(AWS_S3_CUSTOM_DOMAIN)

#############
#COMPRESSION#
#############
INSTALLED_APPS += ('compressor',)
COMPRESS_ENABLED = True
STATICFILES_FINDERS += ('compressor.finders.CompressorFinder',)
COMPRESS_CSS_FILTERS = [
    'compressor.filters.css_default.CssAbsoluteFilter',
    #'compressor.filters.cssmin.CSSMinFilter',
]
COMPRESS_PRECOMPILERS = (
    ('text/less', 'lessc {infile} {outfile}'),
)
COMPRESS_STORAGE = STATICFILES_STORAGE


############
# DATABASE #
############
INSTALLED_APPS += (
    'south',
)
DATABASES = {'default': dj_database_url.config(default='postgres://saul@localhost/django_canadanewyork')}


INSTALLED_APPS += ('django.contrib.sites',)
SITE_ID = 1


###########
# TESTING #
###########
TEST_RUNNER = 'discover_runner.DiscoverRunner'
TEST_DISCOVER_TOP_LEVEL = SITE_ROOT
TEST_DISCOVER_ROOT = rel_path('tests')
SOUTH_TESTS_MIGRATE = False


############
# SECURITY #
############

SECURE_FRAME_DENY = True
SECURE_BROWSER_XSS_FILTER = True
SESSION_COOKIE_SECURE = False
SECURE_CONTENT_TYPE_NOSNIFF = True
MIDDLEWARE_CLASSES += ('django.middleware.csrf.CsrfViewMiddleware',)


###########
# LOGGING #
###########
INSTALLED_APPS += (
    'raven.contrib.django.raven_compat',
)


MIDDLEWARE_CLASSES += (
    'raven.contrib.django.raven_compat.middleware.SentryResponseErrorIdMiddleware',
    'raven.contrib.django.raven_compat.middleware.Sentry404CatchMiddleware',
)

TEMPLATE_CONTEXT_PROCESSORS += (
    'libs.common.context_processors.sentry_dsn',
)

LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'root': {
        'level': 'DEBUG',
        'handlers': ['console', 'sentry'],
    },
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s'
        },
    },
    'handlers': {
        'sentry': {
            'level': 'WARNING',
            'class': 'raven.contrib.django.raven_compat.handlers.SentryHandler',
        },
        'console': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose'
        }
    },
    'loggers': {
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

########
# MISC #
########
INSTALLED_APPS += ('django_extensions',)
INSTALLED_APPS += ('django.contrib.sitemaps',)
