import djcelery
import socket
import os
from django.conf import global_settings

def rel_path(ending):
    return os.path.abspath(os.path.join(os.path.dirname(__file__), str(ending)))

########
#Gondor
########
try:
    from local_settings import *

except ImportError:
    pass

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
    'canada.search',
    'canada.frontpage',
   )

########
#Packages
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
djcelery.setup_loader()

INSTALLED_APPS += (
    'djcelery',
    'djcelery_email',
    'celery',
   )

EMAIL_HOST = "smtp.gmail.com"
EMAIL_PORT = 587
EMAIL_HOST_USER = "saul.shanabrook@gmail.com"
EMAIL_HOST_PASSWORD = "3j}s^52G-qH69%kY"
EMAIL_USE_TLS = True
EMAIL_BACKEND = 'djcelery_email.backends.CeleryEmailBackend'

########
#Django
########
SITE_ID = 1
DEBUG = False

INSTALLED_APPS += (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.flatpages',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.admin',
    'django.contrib.staticfiles',
    'django.contrib.markup',
   )

#Static/Media
STATIC_URL = '/static/'
STATICFILES_DIRS = (
    ('canada', rel_path('static')),
   )
MEDIA_URL = '/media/'

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


########
#Security
########
SECURE_FRAME_DENY = True
SECURE_HSTS_SECONDS = 1
SESSION_COOKIE_HTTPONLY = True
USE_I18N = False
SECRET_KEY = '*itk&52%kmo)f0+ase$uvsy6cmz04c@xr#7$n+bn7_=3wv0lz4'
INTERNAL_IPS = '127.0.0.1'
global_settings.MIDDLEWARE_CLASSES += (
    'django.middleware.csrf.CsrfViewMiddleware',
)
global_settings.TEMPLATE_CONTEXT_PROCESSORS += (
    'django.core.context_processors.csrf',
   )

########
#Debug
########
GLOBAL_DEBUG = True
LOCAL_DEBUG = True

DEBUG = False
if (GLOBAL_DEBUG and socket.gethostname() != 'Sauls-Macbook.local')  or (LOCAL_DEBUG and socket.gethostname() == 'Sauls-Macbook.local'):
    DEBUG = True
    INSTALLED_APPS += (
        'django_extensions',
        'debug_toolbar',
        )
    global_settings.MIDDLEWARE_CLASSES += (
        'debug_toolbar.middleware.DebugToolbarMiddleware',
        )
    global_settings.TEMPLATE_CONTEXT_PROCESSORS += (
        'django.core.context_processors.request',
        )
TEMPLATE_DEBUG = DEBUG
