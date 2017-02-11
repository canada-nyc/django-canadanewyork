from datetime import datetime, timedelta

import environ

root = environ.Path(__file__) - 2

env = environ.Env(
    DEBUG=(bool, False),
)


def insert_after(tuple_, index_item, new_item):
    '''
    Used to insert a middleware class after another one.
    '''
    list_ = list(tuple_)
    list_.insert(list_.index(index_item) + 1, new_item)
    return tuple(list_)

#############
# TEMPLATES #
#############
INSTALLED_APPS = ('sekizai',)
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [root('templates')],
        'APP_DIRS': False,
        'OPTIONS': {
            'context_processors': [
                'sekizai.context_processors.sekizai',
            ],
            'loaders': [
                'django.template.loaders.filesystem.Loader',
                'django.template.loaders.app_directories.Loader',
            ]
        },
    },
]

SHOW_BOOKS = env.bool('CANADA_SHOW_BOOKS', False)
SNIPCART_API_KEY = env('CANADA_SNIPCART_API_KEY')
GOOGLE_TAG_MANAGER_ID = env.str('CANADA_GOOGLE_TAG_MANAGER_ID', "")

##################
# DJANGO DEFAULT #
##################
SECRET_KEY = env('SECRET_KEY')
WSGI_APPLICATION = 'wsgi.application'
ROOT_URLCONF = 'configs.urls'
PREPEND_WWW = False
INSTALLED_APPS += ('django.contrib.sites', )
SITE_ID = 1
# Disable translation
USE_I18N = False

MIDDLEWARE_CLASSES = (
    'dumper.middleware.UpdateCacheMiddleware',
    'django.middleware.gzip.GZipMiddleware',
    'django.middleware.http.ConditionalGetMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'url_tracker.middleware.URLChangePermanentRedirectMiddleware',
    'dumper.middleware.FetchFromCacheMiddleware',
)

TEMPLATES[0]['OPTIONS']['context_processors'] += [
    'django.core.context_processors.request',
    "django.template.context_processors.debug",
    "django.template.context_processors.tz",  # Time zone support
]

########
# MISC #
########
INSTALLED_APPS += ('django.contrib.sitemaps',)
INSTALLED_APPS += ('django.contrib.flatpages',)
INSTALLED_APPS += ('clear_cache',)


##########
# CANADA #
##########
INSTALLED_APPS += (
    'apps.artists',
    'apps.exhibitions',
    'apps.press',
    'apps.books',
    'apps.updates',
    'apps.photos',
    'apps.custompages',

    'libs.common',
)


#############
# URLTRACKER #
#############
INSTALLED_APPS += (
    "url_tracker",
)


#########
# ADMIN #
#########
INSTALLED_APPS += (
    'autocomplete_light',  # must be before django.contrib.admin

    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages'
)
TEMPLATES[0]['OPTIONS']['context_processors'] += [
    "django.contrib.auth.context_processors.auth",
    "django.contrib.messages.context_processors.messages"
]

SESSION_ENGINE = "django.contrib.sessions.backends.cached_db"

INSTALLED_APPS += (
    'libs.ckeditor',
    'adminsortable2',
)
CKEDITOR_CLASS = 'user-created'


##########
# IMAGES #
##########
INSTALLED_APPS += ('simpleimages',)
if env.bool('CANADA_QUEUE_ASYNC'):
    SIMPLEIMAGES_TRANSFORM_CALLER = 'simpleimages.callers.celery'
CANADA_IMAGE_DIMENSION_FIELDS = env('CANADA_IMAGE_DIMENSION_FIELDS')

###########
# DATABASE #
###########
DATABASES = {
    'default': env.db()
}


#########
# QUEUE #
#########
INSTALLED_APPS += ('kombu.transport.django',)
BROKER_URL = 'django://'

CELERY_ALWAYS_EAGER = not env.bool('CANADA_QUEUE_ASYNC')


###########
# STORAGE #
###########
# Static
INSTALLED_APPS += (
    'django.contrib.staticfiles',
    'whitenoise',
)

STATICFILES_DIRS = (
    # Static files in top level directory `static` are accessible under the
    # `canada` path. For example, the file located at `static/images/favicon`
    # would be accessible via {{ static prefix }}/canada/images/favicon
    ('canada', root('static')),
)

TEMPLATES[0]['OPTIONS']['context_processors'] += [
    "django.template.context_processors.static",
]

STATICFILES_STORAGE = 'whitenoise.django.GzipManifestStaticFilesStorage'

STATIC_URL = '/static/'
STATIC_ROOT = root('.static')

# Media
TEMPLATES[0]['OPTIONS']['context_processors'] += [
    "django.template.context_processors.media",
]

if not env.bool('CANADA_STORAGE_S3'):
    MEDIA_URL = '/media/'
    MEDIA_ROOT = root('.media')
else:
    DEFAULT_FILE_STORAGE = "django_s3_storage.storage.S3Storage"

    INSTALLED_APPS += (
        'django_s3_storage',
    )

    AWS_ACCESS_KEY_ID = env('AWS_ACCESS_KEY_ID')
    AWS_SECRET_ACCESS_KEY = env('AWS_SECRET_ACCESS_KEY')
    AWS_S3_BUCKET_NAME = env('AWS_BUCKET')

    AWS_S3_PUBLIC_URL = '//{}/'.format(AWS_S3_BUCKET_NAME)
    AWS_S3_BUCKET_AUTH = False

    # set's cache-control max-age header
    AWS_S3_MAX_AGE_SECONDS = 60*60*24*365  # 1 year.

    _year_in_future = datetime.utcnow() + timedelta(days=365)
    AWS_S3_METADATA = {
        'Expires': _year_in_future.strftime('%a, %d %b %Y %H:%M:%S UTC')
    }

############
# SECURITY #
############
# Adds extra time to response. Also messes with caching.
# Admin overrides this, so unless we add any forms not in the admin
# no need to enable.
# MIDDLEWARE_CLASSES += ('django.middleware.csrf.CsrfViewMiddleware',)
ALLOWED_HOSTS = (env('CANADA_ALLOWED_HOST'),)


###########
# CACHING #
###########
CACHES = {
    'default': env.cache()
}

if env.bool('CANADA_CACHE_TEMPLATES'):
    TEMPLATES[0]['OPTIONS']['loaders'] = [
        ('django.template.loaders.cached.Loader', TEMPLATES[0]['OPTIONS']['loaders']),
    ]

USE_ETAGS = True

DUMPER_PATH_IGNORE_REGEX = r'^/(?:(?:admin)|(?:autocomplete)|(?:media))/'

#########
# DEBUG #
#########
if env.bool('CANADA_DEBUG'):
    DEBUG = TEMPLATES[0]['OPTIONS']['debug'] = True

if env.bool('CANADA_DEVSERVER'):
    INSTALLED_APPS += (
        'devserver',
    )
    DEVSERVER_MODULES = (
        'devserver.modules.sql.SQLRealTimeModule',
        'devserver.modules.sql.SQLSummaryModule',
        'devserver.modules.profile.ProfileSummaryModule',

        # Modules not enabled by default
        'devserver.modules.cache.CacheSummaryModule',
        # 'devserver.modules.profile.LineProfilerModule',
    )

if env.bool('CANADA_DEBUG_TOOLBAR'):
    INSTALLED_APPS += (
        'debug_toolbar',
    )

    # One way to tell debug-toolbar to run no matter
    # if in debug mode or not.
    # Solution from: https://github.com/django-debug-toolbar/django-debug-toolbar/issues/523#issuecomment-31879680
    DEBUG_TOOLBAR_CONFIG = {
        'SHOW_TOOLBAR_CALLBACK': "%s._true" % __name__,
    }

    def _true(request):
        return True

    MIDDLEWARE_CLASSES = insert_after(
        MIDDLEWARE_CLASSES,
        new_item='debug_toolbar.middleware.DebugToolbarMiddleware',
        index_item='django.middleware.gzip.GZipMiddleware')


###########
# LOGGING #
###########
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'simple': {
            'format': '%(name)s %(levelname)s %(message)s'
        },
    },
    'handlers': {
        'console': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'simple'
        }
    },
    'loggers': {
        'django': {},
    },
    'root': {
        'handlers': ['console', ],
        'level': 'INFO'
    },
}


LOGGING['loggers']['pq'] = {
    'level': 'INFO',
}


if env.bool('CANADA_SENTRY'):
    SENTRY_DSN = env('SENTRY_DSN')
    INSTALLED_APPS += (
        'raven.contrib.django.raven_compat',
    )
    LOGGING['handlers']['sentry'] = {
        'level': 'ERROR',
        'class': 'raven.contrib.django.raven_compat.handlers.SentryHandler',
    }
    LOGGING['root']['handlers'].append('sentry')
