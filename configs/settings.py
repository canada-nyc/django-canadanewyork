import os
import urlparse

import dj_database_url

from django.conf.global_settings import *
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
            ("The variable {} must be set to one of the following: {}"
             "It is set to {} instead").format(
                 var_name,
                 str(possible_options),
                 value
             )
        )
    if value.lower() == 'false':
        return False
    return value

##################
# DJANGO DEFAULT #
##################
SECRET_KEY = get_env_variable('SECRET_KEY')
WSGI_APPLICATION = 'wsgi.application'
DATE_FORMAT = 'F j'
ROOT_URLCONF = 'configs.urls'
PREPEND_WWW = False
INSTALLED_APPS += ('django.contrib.sites',)
SITE_ID = 1
# Disable translation
USE_I18N = False


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
    'apps.updates',
    'apps.photos',

    'libs.common',
    'libs.import_wp'
)


#############
# URLTRACKER #
#############

INSTALLED_APPS += (
    "url_tracker",
)
MIDDLEWARE_CLASSES += (
    'url_tracker.middleware.URLChangePermanentRedirectMiddleware',
)


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

INSTALLED_APPS += ('sekizai',)
TEMPLATE_CONTEXT_PROCESSORS += ('sekizai.context_processors.sekizai',)


#############
# FLATPAGES #
#############
INSTALLED_APPS += ('django.contrib.flatpages',)


##########
# IMAGES #
##########
INSTALLED_APPS += ('simpleimages',)


###########
# DATABASE #
###########
INSTALLED_APPS += (
    'south',
)
SOUTH_TESTS_MIGRATE = False

DATABASES = {
    'default': dj_database_url.config()
}

###########
# TESTING #
###########

if get_env_variable('CANADA_TESTRUNNER'):
    TEST_RUNNER = 'discover_runner.DiscoverRunner'
    TEST_DISCOVER_TOP_LEVEL = rel_path('tests')


###########
# STORAGE #
###########
INSTALLED_APPS += ('django.contrib.staticfiles',)
STATICFILES_DIRS = (
    ('canada', rel_path('static')),
)

_storage_backend = get_env_variable(
    'CANADA_STORAGE',
    possible_options=['local', 's3']
)

if _storage_backend == 'local':
    DEFAULT_FILE_STORAGE = 'django.core.files.storage.FileSystemStorage'

    STATIC_URL = '/static/'
    STATIC_ROOT = rel_path('tmp/static')

    MEDIA_ROOT = rel_path('tmp/media')
    MEDIA_URL = '/media/'
elif _storage_backend == 's3':
    DEFAULT_FILE_STORAGE = 'storages.backends.s3boto.S3BotoStorage'

    INSTALLED_APPS += (
        'storages',
    )
    AWS_ACCESS_KEY_ID = get_env_variable('AWS_ACCESS_KEY_ID')
    AWS_SECRET_ACCESS_KEY = get_env_variable('AWS_SECRET_ACCESS_KEY')
    AWS_STORAGE_BUCKET_NAME = get_env_variable('AWS_BUCKET')
    AWS_S3_CUSTOM_DOMAIN = AWS_STORAGE_BUCKET_NAME
    AWS_HEADERS = {
        "Cache-Control": "public, max-age=31536000",
    }
    AWS_QUERYSTRING_AUTH = False
    AWS_QUERYSTRING_EXPIRE = 600
    AWS_S3_SECURE_URLS = False
    AWS_IS_GZIPPED = True
    AWS_PRELOAD_METADATA = True

    STATIC_URL = 'http://{}/'.format(AWS_S3_CUSTOM_DOMAIN)

STATICFILES_STORAGE = DEFAULT_FILE_STORAGE

###############
# COMPRESSION #
###############
INSTALLED_APPS += ('compressor',)
COMPRESS_ENABLED = True
COMPRESS_STORAGE = STATICFILES_STORAGE
STATICFILES_FINDERS += ('compressor.finders.CompressorFinder',)
COMPRESS_CSS_FILTERS = [
    'compressor.filters.template.TemplateFilter',
    'compressor.filters.css_default.CssAbsoluteFilter',
    # 'compressor.filters.cssmin.CSSMinFilter',
]
COMPRESS_JS_FILTERS = [
    'configs.filters.UglifyJSFilter'
]
COMPRESS_PRECOMPILERS = (
    ('text/less', 'lessc {infile} {outfile}'),
)
COMPRESS_TEMPLATE_FILTER_CONTEXT = {}


############
# SECURITY #
############
SECURE_FRAME_DENY = True
SECURE_BROWSER_XSS_FILTER = True
SESSION_COOKIE_SECURE = False
SECURE_CONTENT_TYPE_NOSNIFF = True
MIDDLEWARE_CLASSES += ('django.middleware.csrf.CsrfViewMiddleware',)
ALLOWED_HOSTS = (get_env_variable('CANADA_ALLOWED_HOST'),)


###########
# CACHING #
###########
_cache_backend = get_env_variable(
    'CANADA_CACHE',
    possible_options=['redis', 'memory', 'dummy']
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
            'JOHNNY_CACHE': True
        }
    }
elif _cache_backend == 'memory':
    CACHES = {
        'default': {
            'BACKEND': 'johnny.backends.locmem.LocMemCache',
            'LOCATION': 'django_canadanewyork',
            'JOHNNY_CACHE': True
        }
    }
elif _cache_backend == 'dummy':
    CACHES = {
        'default': {
            'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
        }
    }
    DISABLE_QUERYSET_CACHE = True


if get_env_variable('CANADA_CACHE_TEMPLATES'):
    TEMPLATE_LOADERS = (
        ('django.template.loaders.cached.Loader', (
            'django.template.loaders.filesystem.Loader',
            'django.template.loaders.app_directories.Loader',
        )),
    )

MIDDLEWARE_CLASSES += (
    'django.middleware.gzip.GZipMiddleware',
)

# Johny Cache
MIDDLEWARE_CLASSES = (
    'johnny.middleware.LocalStoreClearMiddleware',
    'johnny.middleware.QueryCacheMiddleware',
) + MIDDLEWARE_CLASSES

JOHNNY_MIDDLEWARE_KEY_PREFIX = 'jc'


#########
# DEBUG #
#########

if get_env_variable('CANADA_DEBUG'):
    DEBUG = TEMPLATE_DEBUG = True

    if get_env_variable('CANADA_DEBUG_TOOLBAR'):
        INSTALLED_APPS += (
            'debug_toolbar',
            'debug_toolbar_autoreload',
        )
        MIDDLEWARE_CLASSES += ('debug_toolbar.middleware.DebugToolbarMiddleware',)
        DEBUG_TOOLBAR_CONFIG = {
            'INTERCEPT_REDIRECTS': False,
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

            'debug_toolbar_autoreload.AutoreloadPanel',

        )

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

###########
# LOGGING #
###########
LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'root': {
        'level': get_env_variable('CANADA_CONSOLE_LOGGING_LEVEL'),
        'handlers': ['console'],
    },
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(module)s %(message)s'
        },
    },
    'handlers': {
        'console': {
            'level': get_env_variable('CANADA_CONSOLE_LOGGING_LEVEL'),
            'class': 'logging.StreamHandler',
            'formatter': 'verbose'
        }
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': True,
        },
    }
}

if get_env_variable('CANADA_SENTRY'):
    INSTALLED_APPS += (
        'raven.contrib.django.raven_compat',
    )
    TEMPLATE_CONTEXT_PROCESSORS += (
        'libs.common.context_processors.sentry_dsn',
    )
    LOGGING['loggers'] = {
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
    }

    LOGGING['handlers']['sentry'] = {
        'level': 'ERROR',
        'class': 'raven.contrib.django.raven_compat.handlers.SentryHandler',
    }
    LOGGING['root']['handlers'].append('sentry')
