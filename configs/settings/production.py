import os


class HerokuMemcache(object):
    CACHES = {
        'default': {
            'BACKEND': 'django_pylibmc.memcached.PyLibMCCache',
            'LOCATION': os.environ.get('MEMCACHIER_SERVERS'),
            'TIMEOUT': 500,
            'BINARY': True,
        }
    }


class SecureFrameDeny(object):
    SECURE_FRAME_DENY = True


class GZip(object):
    @property
    def MIDDLEWARE_CLASSES(self):
        return (
            'django.middleware.gzip.GZipMiddleware',
        ) + super(GZip, self).MIDDLEWARE_CLASSES


class CSRF(object):
    @property
    def MIDDLEWARE_CLASSES(self):
        return (
            'django.middleware.csrf.CsrfViewMiddleware',
        ) + super(CSRF, self).MIDDLEWARE_CLASSES
