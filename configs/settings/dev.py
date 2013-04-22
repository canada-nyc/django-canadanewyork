from .testing import *
from .local_storage import *

#########
# LOCAL #
#########
INTERNAL_IPS = ('127.0.0.1',)
ALLOWED_HOSTS = ['localhost', '127.0.0.1', '127.0.0.1:8000']

#########
# DEBUG #
#########
DEBUG = TEMPLATE_DEBUG = True

INSTALLED_APPS += ('debug_toolbar',)
MIDDLEWARE_CLASSES += ('debug_toolbar.middleware.DebugToolbarMiddleware',)
DEBUG_TOOLBAR_CONFIG = {
    'INTERCEPT_REDIRECTS': False,
}

TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
)
