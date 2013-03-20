import imp
import os

import dj_database_url

from django.conf.global_settings import *


##################
# DJANGO DEFAULT #
##################
SITE_ROOT = os.path.dirname(imp.find_module('manage')[1])


def rel_path(relative_path):
        '''
        given any path relative to the `SITE_ROOT`, returns the full path
        '''
        return os.path.normpath(os.path.join(SITE_ROOT, relative_path))

SECRET_KEY = os.environ.get('SECRET_KEY', '*YSHFUIH&GAHJBJCZKCY)P#R')
WSGI_APPLICATION = 'manage.application'
DATE_FORMAT = 'F j'
ROOT_URLCONF = 'configs.urls'
PREPEND_WWW = False

##########
# CANADA #
##########
INSTALLED_APPS = (
    'apps.artists',
    'apps.exhibitions',
    'apps.press',
    'apps.updates',
    'apps.info',
    'apps.photos',

    'libs.common',
)


##########
# MODELS #
##########
INSTALLED_APPS += (
    "url_tracker",
)
MIDDLEWARE_CLASSES += ('url_tracker.middleware.URLChangePermanentRedirectMiddleware',)


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

INSTALLED_APPS += ('bootstrapform',)

INSTALLED_APPS += ('markdown_deux',)
MARKDOWN_DEUX_STYLES = {
    "default": {
        "safe_mode": "escape",
    },
}

INSTALLED_APPS += ('sekizai',)
TEMPLATE_CONTEXT_PROCESSORS += ('sekizai.context_processors.sekizai',)


##############
# THUMBNAILS #
##############
INSTALLED_APPS += ('simpleimages',)

###########
# STORAGE #
###########
INSTALLED_APPS += ('django.contrib.staticfiles',)
STATICFILES_DIRS = (
    ('canada', rel_path('static')),
)

COMPRESS_ENABLED = True
INSTALLED_APPS += ('compressor',)
STATICFILES_FINDERS += ('compressor.finders.CompressorFinder',)
COMPRESS_CSS_FILTERS = [
    'compressor.filters.css_default.CssAbsoluteFilter',
    #'compressor.filters.cssmin.CSSMinFilter',
]
COMPRESS_PRECOMPILERS = (
    ('text/less', 'lessc {infile} {outfile}'),
)


############
# DATABASE #
############
INSTALLED_APPS += (
    'south',
)
DATABASES = {'default': dj_database_url.config(default='postgres://saul@localhost/django_canadanewyork')}


#########
# EMAIL #
#########
EMAIL_HOST = "smtp.gmail.com"
EMAIL_PORT = 587
EMAIL_HOST_USER = "s.shanabrook@gmail.com"
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD', '')
EMAIL_USE_TLS = True

INSTALLED_APPS += ('django.contrib.sites',)
SITE_ID = 1


###########
# TESTING #
###########
TEST_RUNNER = 'discover_runner.DiscoverRunner'
TEST_DISCOVER_TOP_LEVEL = SITE_ROOT
TEST_DISCOVER_ROOT = rel_path('tests')
SOUTH_TESTS_MIGRATE = False


############
# SECURITY #
############

SECURE_FRAME_DENY = True
SECURE_BROWSER_XSS_FILTER = True
SESSION_COOKIE_SECURE = False
SECURE_CONTENT_TYPE_NOSNIFF = True


########
# MISC #
########
INSTALLED_APPS += ('django_extensions',)
INSTALLED_APPS += ('django.contrib.sitemaps',)
