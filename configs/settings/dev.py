from .common import *


#########
# LOCAL #
#########
INTERNAL_IPS = ('127.0.0.1',)

'''
###########
# STORAGE #
###########
MEDIA_ROOT = rel_path('tmp/media/')
STATIC_ROOT = rel_path('tmp/static/')

MEDIA_URL = '/media/'
STATIC_URL = '/static/'

'''

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


#########
# DEBUG #
#########
#DEBUG = TEMPLATE_DEBUG = True

INSTALLED_APPS += ('debug_toolbar',)
MIDDLEWARE_CLASSES += ('debug_toolbar.middleware.DebugToolbarMiddleware',)
DEBUG_TOOLBAR_CONFIG = {
    'INTERCEPT_REDIRECTS': False,
}

'''
# https://github.com/tomchristie/django-pdb
INSTALLED_APPS += ('django_pdb',)
MIDDLEWARE_CLASSES += ('django_pdb.middleware.PdbMiddleware',)
'''
