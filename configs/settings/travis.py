from .common import *


###########
# Caching #
###########
TEMPLATE_LOADERS = (
    ('django.template.loaders.cached.Loader', (
        'django.template.loaders.filesystem.Loader',
        'django.template.loaders.app_directories.Loader',
    )),
)

CACHES = {
    'default': {
        'BACKEND': 'django_pylibmc.memcached.PyLibMCCache',
        'LOCATION': os.environ.get('MEMCACHIER_SERVERS'),
        'TIMEOUT': 500,
        'BINARY': True,
    }
}

MIDDLEWARE_CLASSES += ('django.middleware.gzip.GZipMiddleware',)


###########
# STORAGE #
###########
INSTALLED_APPS += ('storages',)
DEFAULT_FILE_STORAGE = THUMBNAIL_DEFAULT_STORAGE = STATICFILES_STORAGE = 'storages.backends.s3boto.S3BotoStorage'
AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY')
AWS_STORAGE_BUCKET_NAME = os.environ.get('AWS_BUCKET')
AWS_PRELOAD_METADATA = True
COMPRESS_URL = 'https://{}.s3.amazonaws.com/'.format(AWS_STORAGE_BUCKET_NAME)


############
# SECURITY #
############
SECURE_FRAME_DENY = True
MIDDLEWARE_CLASSES += ('django.middleware.csrf.CsrfViewMiddleware',)
