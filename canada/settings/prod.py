from .common import *


#from memcacheify import memcacheify
import dj_database_url


DEBUG = False
TEMPLATE_DEBUG = DEBUG

########
#Cache
########

#CACHES = memcacheify()  # http://rdegges.github.com/django-heroku-memcacheify/
# Run heroku addons:add memcachier:25 for free 25m
MIDDLEWARE_CLASSES = ('django.middleware.gzip.GZipMiddleware',) + MIDDLEWARE_CLASSES

########
#Databse
########
DATABASES = {'default': dj_database_url.config(default='postgres://localhost')}

########
#Server
########
INSTALLED_APPS += ('gunicorn',)
INTERNAL_IPS = ('0.0.0.0',)

########
#Email
########
EMAIL_HOST = "smtp.gmail.com"
EMAIL_PORT = 587
EMAIL_HOST_USER = "saul.shanabrook@gmail.com"
EMAIL_HOST_PASSWORD = ""
EMAIL_USE_TLS = True

########
#Security
########
SECURE_FRAME_DENY = True
TEMPLATE_CONTEXT_PROCESSORS += ('django.core.context_processors.csrf',)
CSRF_COOKIE_DOMAIN = '.canadanewyork.com'
PREPEND_WWW = True