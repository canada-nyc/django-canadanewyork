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
INSTALLED_APPS += (
    'storages',
    's3_folder_storage',
)
AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY')
AWS_STORAGE_BUCKET_NAME = AWS_S3_CUSTOM_DOMAIN = os.environ.get('AWS_BUCKET')
AWS_PRELOAD_METADATA = True
AWS_QUERYSTRING_AUTH = False

DEFAULT_FILE_STORAGE = THUMBNAIL_DEFAULT_STORAGE = 's3_folder_storage.s3.DefaultStorage'
DEFAULT_S3_PATH = "media"
STATICFILES_STORAGE = COMPRESS_STORAGE = 's3_folder_storage.s3.StaticStorage'
STATIC_S3_PATH = "static"


MEDIA_ROOT = '/{}/'.format(DEFAULT_S3_PATH)
MEDIA_URL = 'https://{}/{}/'.format(AWS_STORAGE_BUCKET_NAME, DEFAULT_S3_PATH)

STATIC_ROOT = '/{}/'.format(STATIC_S3_PATH)
STATIC_URL = 'https://{}/{}/'.format(AWS_STORAGE_BUCKET_NAME, STATIC_S3_PATH)

ADMIN_MEDIA_PREFIX = STATIC_URL + 'admin/'


############
# SECURITY #
############
SECURE_FRAME_DENY = True
MIDDLEWARE_CLASSES += ('django.middleware.csrf.CsrfViewMiddleware',)
