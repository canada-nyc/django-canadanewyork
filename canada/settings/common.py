from django.conf.global_settings import *

from canada.functions import rel_path, add_to_middleware


########
#CANADA
########
CANADA_SLIDER_IMAGE_SIZE = 'x300'
CANADA_FRONTPAGE_IMAGE_SIZE = 'x400'
CANADA_UPDATES_IMAGE_SIZE = 'x400'
INSTALLED_APPS = (
    'canada.artists',
    'canada.exhibitions',
    'canada.press',
    'canada.updates',
    'canada.bulkmail',
    'canada.updates',
  )


########
#External Packages
########
INSTALLED_APPS += (
    'south',
    'grappelli',
    'sorl.thumbnail',
  )

GRAPPELLI_ADMIN_TITLE = 'CANADA'


########
#Email
########
EMAIL_HOST = "smtp.gmail.com"
EMAIL_PORT = 587
EMAIL_HOST_USER = "saul.shanabrook@gmail.com"
EMAIL_HOST_PASSWORD = "3j}s^52G-qH69%kY"
EMAIL_USE_TLS = True


########
#Django
########
DEBUG = False

INSTALLED_APPS += (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.admin',
    'django.contrib.staticfiles',
    'django.contrib.markup',
  )

#Static/Media
STATICFILES_DIRS = (
    ('canada', rel_path('static/')),
  )

MEDIA_URL = '/media/'

STATIC_URL = '/static/'
STATIC_ROOT = rel_path('../static/')
MEDAIA_ROOT = rel_path('../media')


#Admin
LOGIN_URL = '/admin/'
ADMIN_MEDIA_PREFIX = STATIC_URL + "grappelli/"
ADMINS = (
    ('Saul Shanabrook', 'saul.shanabrook@gmail.com'),
  )


#Urls
ROOT_URLCONF = 'canada.urls'

#Templates
TEMPLATE_DIRS = (
    rel_path('templates'),
  )

MIDDLEWARE_CLASSES = add_to_middleware(MIDDLEWARE_CLASSES,
                                       'django.middleware.gzip.GZipMiddleware',
                                       prepend=True)
DATE_FORMAT = 'F j, Y'

########
#Testing
########
TEST_RUNNER = 'discover_runner.DiscoverRunner'
TEST_DISCOVER_TOP_LEVEL = rel_path()
TEST_DISCOVER_ROOT = rel_path('tests')


########
#Security
########
SECURE_FRAME_DENY = True
SECRET_KEY = '*itk&52%kmo)f0+ase$uvsy6cmz04c@xr#7$n+bn7_=3wv0lz4'

TEMPLATE_CONTEXT_PROCESSORS += ('django.core.context_processors.csrf',)
