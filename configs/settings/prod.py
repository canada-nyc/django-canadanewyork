from .common import *


############
# SECURITY #
############
ALLOWED_HOSTS = (
    "{HEROKU_APP_NAME}.herokuapp.com".format(
        HEROKU_APP_NAME=os.environ.get('heroku_app_name'),
    ),
)


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
        'level': 'INFO',
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
            'level': 'WARNING',
            'handlers': ['console'],
            'propagate': False,
        },
        'sentry.errors': {
            'level': 'WARNING',
            'handlers': [],
            'propagate': False,
        },
    },
}
