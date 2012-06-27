from memcacheify import memcacheify

from canada.settings.base import *


DEBUG = False

########
#Cache
########

CACHES = memcacheify()  # http://rdegges.github.com/django-heroku-memcacheify/
# Run heroku addons:add memcachier:25 for free 25m
