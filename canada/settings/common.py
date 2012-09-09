from os import path, environ

import canada


SITE_ROOT = path.dirname(path.realpath(canada.__file__))

########
#Default
########
TEMPLATE_CONTEXT_PROCESSORS = (
    "django.contrib.auth.context_processors.auth",
    "django.core.context_processors.debug",
    "django.core.context_processors.i18n",
    "django.core.context_processors.media",
    "django.core.context_processors.static",
    "django.core.context_processors.tz",
    "django.contrib.messages.context_processors.messages"
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
)

STATICFILES_FINDERS = (
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
)
########
#CANADA
########
CANADA_IMAGE_SIZE = 'x300'
CANADA_FRONTPAGE_IMAGE_SIZE = 'x400'
CANADA_ADMIN_THUMBS_SIZE = 'x60'

INSTALLED_APPS = (
    'canada.apps.artists',
    'canada.apps.exhibitions',
    'canada.apps.press',
    'canada.apps.updates',
    'canada.apps.bulkmail',
    'canada.apps.updates',
    'canada.apps.frontpage',
    'canada.apps.info',
    'canada.apps.base'
)

TEMPLATE_CONTEXT_PROCESSORS += ('canada.context_processors.image_size',)

########
#Email
########
EMAIL_HOST = "smtp.gmail.com"
EMAIL_PORT = 587
EMAIL_HOST_USER = "s.shanabrook@gmail.com"
EMAIL_HOST_PASSWORD = environ.get('EMAIL_HOST_PASSWORD', '')
EMAIL_USE_TLS = True


########
#External Packages
########
INSTALLED_APPS += (
    'south',
    'grappelli',
    'sorl.thumbnail',
    'smart_selects',
    'bootstrapform',
    'django_rq',
    'compressor',)

GRAPPELLI_ADMIN_TITLE = 'CANADA'

STATICFILES_FINDERS += ('compressor.finders.CompressorFinder',)
COMPRESS_ENABLED = True
COMPRESS_CSS_FILTERS = [
    'compressor.filters.css_default.CssAbsoluteFilter',
    'compressor.filters.cssmin.CSSMinFilter'
]

COMPRESS_PRECOMPILERS = (
    ('text/less', 'lessc -x {infile} {outfile}'),
)


########
#Django Customize
########
ADMINS = (
    ('Saul Shanabrook', 'saul.shanabrook@gmail.com'),
)

APPEND_SLASH = True

DATE_FORMAT = 'F j, Y'


########
#Security
########
TEMPLATE_CONTEXT_PROCESSORS += ('django.core.context_processors.csrf',)


########
#Django Boilerplate
########
INSTALLED_APPS += (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.admin',
    'django.contrib.staticfiles',
    'django.contrib.markup',
    'django.contrib.sites',
)

SITE_ID = 1
SECRET_KEY = environ.get('SECRET_KEY', '*YSHFUIH&GAHJBJCZKCY)P#R')
WSGI_APPLICATION = 'manage.application'

STATICFILES_DIRS = (
    ('canada', path.join(SITE_ROOT, 'static')),
)

MEDIA_URL = '/media/'
MEDIA_ROOT = path.normpath(path.join(SITE_ROOT, '../media/'))

STATIC_URL = '/static/'
STATIC_ROOT = path.normpath(path.join(SITE_ROOT, '../static/'))

FIXTURE_DIRS = (path.join(SITE_ROOT, 'fixtures'),)

LOGIN_URL = '/admin/'
ADMIN_MEDIA_PREFIX = STATIC_URL + "grappelli/"

ROOT_URLCONF = 'canada.urls'

TEMPLATE_DIRS = (
    path.join(SITE_ROOT, 'templates'),
)
