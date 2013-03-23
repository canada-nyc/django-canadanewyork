import os

import dj_database_url

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
    'apps.info',
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

INSTALLED_APPS += ('bootstrapform',)

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
# STORAGE #
###########
INSTALLED_APPS += ('django.contrib.staticfiles',)
STATICFILES_DIRS = (
    ('canada', rel_path('static')),
)


INSTALLED_APPS += (
    'storages',
    's3_folder_storage',
)
AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY')
AWS_STORAGE_BUCKET_NAME = os.environ.get('AWS_BUCKET')
AWS_HEADERS = {
    "Cache-Control": "public, max-age=86400",
}
AWS_QUERYSTRING_AUTH = False
AWS_S3_SECURE_URLS = False
AWS_IS_GZIPPED = True
AWS_PRELOAD_METADATA = True


DEFAULT_FILE_STORAGE = 's3_folder_storage.s3.DefaultStorage'
STATICFILES_STORAGE = COMPRESS_STORAGE = 's3_folder_storage.s3.StaticStorage'

# Use by s3_folder_storage to save the static and other media to a path on the
# bucket
DEFAULT_S3_PATH = "media"
STATIC_S3_PATH = "static"

# The static URL is irrelevent for and alternative storage backend
STATIC_URL = '_/'


############
# DATABASE #
############
INSTALLED_APPS += (
    'south',
)
DATABASES = {'default': dj_database_url.config(default='postgres://saul@localhost/django_canadanewyork')}


#########
# EMAIL #
#########
EMAIL_HOST = "smtp.gmail.com"
EMAIL_PORT = 587
EMAIL_HOST_USER = "s.shanabrook@gmail.com"
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD', '')
EMAIL_USE_TLS = True

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
        'LOCATION': os.environ.get('MEMCACHIER_SERVERS', 'localhost:11211'),
        'TIMEOUT': 3,
        #'BINARY': True,
    }
}

SESSION_ENGINE = "django.contrib.sessions.backends.signed_cookies"
MESSAGE_STORAGE = "django.contrib.messages.storage.cookie.CookieStorage"
THUMBNAIL_KVSTORE = 'sorl.thumbnail.kvstores.redis_kvstore.KVStore'

MIDDLEWARE_CLASSES += ('django.middleware.cache.FetchFromCacheMiddleware',)
# Must be first
MIDDLEWARE_CLASSES = ('django.middleware.cache.UpdateCacheMiddleware',) + MIDDLEWARE_CLASSES

SESSION_ENGINE = "django.contrib.sessions.backends.cached_db"


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

########
# MISC #
########
INSTALLED_APPS += ('django_extensions',)
INSTALLED_APPS += ('django.contrib.sitemaps',)
