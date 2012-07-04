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

########
#Databse
########
DATABASES = {'default': dj_database_url.config(default='postgres://localhost')}

########
# Server
########
INSTALLED_APPS += ('gunicorn',)
INTERNAL_IPS = ('0.0.0.0',)
