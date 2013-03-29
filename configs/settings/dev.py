from .common import *


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

if not os.environ.get('USE_S3_IN_DEV', None):
    STATICFILES_STORAGE = COMPRESS_STORAGE = DEFAULT_FILE_STORAGE = 'django.core.files.storage.FileSystemStorage'
    STATIC_URL = '/static/'
    STATIC_ROOT = rel_path('tmp/static')

    MEDIA_ROOT = rel_path('tmp/media')
    MEDIA_URL = '/media/'
