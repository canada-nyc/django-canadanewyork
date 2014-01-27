import os
import urlparse
from datetime import datetime, timedelta
import logging

import dj_database_url
from memcacheify import memcacheify

from django.core.exceptions import ImproperlyConfigured

from libs.common.utils import rel_path


def get_env_variable(var_name, possible_options=[]):
    try:
        value = os.environ[var_name]
    except KeyError:
        message = "Set the {} environment variable".format(var_name)
        if possible_options:
            message += 'Possible options are {}'.format(str(possible_options))
        raise ImproperlyConfigured(message)
    if possible_options and value not in possible_options:
        raise ImproperlyConfigured(
            "The variable {} must be set to one of the following: {} "
            "It is set to '{}'' instead".format(
                var_name,
                str(possible_options),
                value
            )
        )
    if value.lower() == 'false':
        return False
    if value.lower() == 'true':
        return True
    return value

##################
# DJANGO DEFAULT #
##################
SECRET_KEY = get_env_variable('SECRET_KEY')
WSGI_APPLICATION = 'wsgi.application'
ROOT_URLCONF = 'configs.urls'
PREPEND_WWW = False
INSTALLED_APPS = ('django.contrib.sites', 'django.contrib.flatpages',)
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

TEMPLATE_CONTEXT_PROCESSORS = (
    "django.core.context_processors.debug",
    "django.core.context_processors.tz",  # Time zone support
)

########
# MISC #
########
INSTALLED_APPS += ('django_extensions',)
INSTALLED_APPS += ('django.contrib.sitemaps',)
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
    'grappelli',

    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages'
)
TEMPLATE_CONTEXT_PROCESSORS += (
    "django.contrib.auth.context_processors.auth",
    "django.contrib.messages.context_processors.messages"
)

GRAPPELLI_ADMIN_TITLE = 'canada'
SESSION_ENGINE = "django.contrib.sessions.backends.cached_db"


#############
# TEMPLATES #
#############
TEMPLATE_DIRS = (rel_path('templates'), )

INSTALLED_APPS += ('sekizai',)
TEMPLATE_CONTEXT_PROCESSORS += ('sekizai.context_processors.sekizai',)


##########
# IMAGES #
##########
INSTALLED_APPS += ('simpleimages',)
SIMPLEIMAGES_TRANSFORM_CALLER = 'configs.queues.enqueue'


###########
# DATABASE #
###########
INSTALLED_APPS += (
    'south',
)
SOUTH_TESTS_MIGRATE = False
SOUTH_DATABASE_ADAPTERS = {
    'default': 'south.db.postgresql_psycopg2'
}
DATABASES = {
    'default': dj_database_url.config()
}
DATABASES['default']['ENGINE'] = 'django_postgrespool'


#########
# QUEUE #
#########
INSTALLED_APPS += ('pq',)

QUEUE_ASYNC = get_env_variable('CANADA_QUEUE_ASYNC')

# not default in django 1.5
DATABASES['default']['OPTIONS'] = {'autocommit': True}
PQ_QUEUE_CACHE = True


###########
# TESTING #
###########
if get_env_variable('CANADA_TESTRUNNER'):
    TEST_RUNNER = 'discover_runner.DiscoverRunner'


###########
# STORAGE #
###########
INSTALLED_APPS += ('django.contrib.staticfiles',)
STATICFILES_DIRS = (
    ('canada', rel_path('static')),
)
TEMPLATE_CONTEXT_PROCESSORS += (
    "django.core.context_processors.media",
    "django.core.context_processors.static",
)
_storage_backend = get_env_variable(
    'CANADA_STORAGE',
    possible_options=['local', 's3']
)
if _storage_backend == 'local':
    STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.CachedStaticFilesStorage'

    STATIC_URL = '/static/'
    STATIC_ROOT = rel_path('tmp/static')

    MEDIA_URL = '/media/'
    MEDIA_ROOT = rel_path('tmp/media')

elif _storage_backend == 's3':
    DEFAULT_FILE_STORAGE = 'storages.backends.s3boto.S3BotoStorage'
    STATICFILES_STORAGE = 'configs.storage_backends.S3HashedFilesStorage'

    INSTALLED_APPS += (
        'storages',
    )
    AWS_ACCESS_KEY_ID = get_env_variable('AWS_ACCESS_KEY_ID')
    AWS_SECRET_ACCESS_KEY = get_env_variable('AWS_SECRET_ACCESS_KEY')
    AWS_STORAGE_BUCKET_NAME = get_env_variable('AWS_BUCKET')
    AWS_S3_CUSTOM_DOMAIN = AWS_STORAGE_BUCKET_NAME
    _year_in_future = datetime.utcnow() + timedelta(days=365)
    AWS_HEADERS = {
        "Cache-Control": "public, max-age=31536000",
        'Expires': _year_in_future.strftime('%a, %d %b %Y %H:%M:%S UTC')
    }
    AWS_QUERYSTRING_AUTH = False
    AWS_QUERYSTRING_EXPIRE = 600
    AWS_S3_SECURE_URLS = False
    AWS_IS_GZIPPED = True
    AWS_PRELOAD_METADATA = True

    STATIC_URL = 'http://{}/'.format(AWS_S3_CUSTOM_DOMAIN)


############
# SECURITY #
############
# Adds extra time to response. Also messes with caching.
# Admin overrides this, so unless we add any forms not in the admin
# no need to enable.
# MIDDLEWARE_CLASSES += ('django.middleware.csrf.CsrfViewMiddleware',)
ALLOWED_HOSTS = (get_env_variable('CANADA_ALLOWED_HOST'),)


###########
# CACHING #
###########
_cache_backend = get_env_variable(
    'CANADA_CACHE',
    possible_options=['redis', 'memcache', 'memory', 'database', 'dummy']
)

if _cache_backend == 'redis':
    redis_url = urlparse.urlparse(get_env_variable('REDISCLOUD_URL'))

    CACHES = {
        'default': {
            "BACKEND": "redis_cache.cache.RedisCache",
            'LOCATION': '{}:{}:{}'.format(redis_url.hostname, redis_url.port, 0),
            'OPTIONS': {
                'PASSWORD': redis_url.password,
            },
        }
    }
elif _cache_backend == 'memcache':
    CACHES = memcacheify()
elif _cache_backend == 'database':
    CACHES = {
        'default': {
            'BACKEND': 'django.core.cache.backends.db.DatabaseCache',
            'LOCATION': 'cache',
        }
    }
elif _cache_backend == 'memory':
    CACHES = {
        'default': {
            'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
            'LOCATION': 'django_canadanewyork',
        }
    }
elif _cache_backend == 'dummy':
    CACHES = {
        'default': {
            'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
        }
    }


if get_env_variable('CANADA_CACHE_TEMPLATES'):
    TEMPLATE_LOADERS = (
        ('django.template.loaders.cached.Loader', (
            'django.template.loaders.filesystem.Loader',
            'django.template.loaders.app_directories.Loader',
        )),
    )

USE_ETAGS = True

DUMPER_PATH_IGNORE_REGEX = r'^/(?:(?:admin)|(?:grappelli))/'

#########
# DEBUG #
#########
if get_env_variable('CANADA_DEBUG'):
    DEBUG = TEMPLATE_DEBUG = True

if get_env_variable('CANADA_DEVSERVER'):
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

if get_env_variable('CANADA_DEBUG_TOOLBAR'):
    INSTALLED_APPS += (
        'debug_toolbar',
    )
    MIDDLEWARE_CLASSES += ('debug_toolbar.middleware.DebugToolbarMiddleware',)
    DEBUG_TOOLBAR_CONFIG = {
        'INTERCEPT_REDIRECTS': False,
        'SHOW_TOOLBAR_CALLBACK': lambda _: True,
    }
    DEBUG_TOOLBAR_PANELS = (
        'debug_toolbar.panels.cache.CacheDebugPanel',
        'debug_toolbar.panels.headers.HeaderDebugPanel',
        'debug_toolbar.panels.logger.LoggingPanel',
        'debug_toolbar.panels.profiling.ProfilingDebugPanel',
        'debug_toolbar.panels.request_vars.RequestVarsDebugPanel',
        'debug_toolbar.panels.settings_vars.SettingsVarsDebugPanel',
        'debug_toolbar.panels.signals.SignalDebugPanel',
        'debug_toolbar.panels.sql.SQLDebugPanel',
        'debug_toolbar.panels.template.TemplateDebugPanel',
        'debug_toolbar.panels.timer.TimerDebugPanel',
        'debug_toolbar.panels.version.VersionDebugPanel',
    )

###########
# LOGGING #
###########
LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        'simple': {
            'format': '%(name)s %(levelname)s %(message)s'
        },
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'simple'
        }
    },
    'root': {
        'handlers': ['console', ],
        'level': 'WARNING'
    },
}

if get_env_variable('CANADA_DUMPER_LOG'):
    LOGGING['loggers'] = {
        'dumper': {
            'level': 'DEBUG',
        }
    }

if get_env_variable('CANADA_SENTRY'):
    SENTRY_DSN = get_env_variable('SENTRY_DSN')
    INSTALLED_APPS += (
        'raven.contrib.django.raven_compat',
    )
    LOGGING['handlers']['sentry'] = {
        'level': 'ERROR',
        'class': 'raven.contrib.django.raven_compat.handlers.SentryHandler',
    }
    LOGGING['root']['handlers'].append('sentry')
