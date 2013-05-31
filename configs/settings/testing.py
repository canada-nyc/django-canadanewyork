from .common import *


#########
# TESTING #
#########
# must come after 'south', so that this version of `./manage.py test` takes precedence
INSTALLED_APPS += ('django_nose', )
TEST_RUNNER = 'django_nose.NoseTestSuiteRunner'
NOSE_ARGS = [
    '--with-specplugin',
    '--detailed-errors',
    '--nologcapture',
    '-s'
]

########
# CACHE #
########
DATABASES['default'] = {'ENGINE': 'django.db.backends.sqlite3'}

# CACHES = {
#     'default': {
#         'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
#         'LOCATION': 'unique-snowflake'
#     }
# }
