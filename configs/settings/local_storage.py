from libs.common.utils import rel_path


STATICFILES_STORAGE = COMPRESS_STORAGE = DEFAULT_FILE_STORAGE = 'django.core.files.storage.FileSystemStorage'
STATIC_URL = '/static/'
STATIC_ROOT = rel_path('tmp/static')

MEDIA_ROOT = rel_path('tmp/media')
MEDIA_URL = '/media/'
