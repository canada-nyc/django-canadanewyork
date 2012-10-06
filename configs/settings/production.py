from . import services


class HerokuMemcache(object):
    try:
        from memcacheify import memcacheify
    except:
        pass
    else:
        CACHES = memcacheify()


class SecureFrameDeny(object):
    SECURE_FRAME_DENY = True


class GZip(object):
    @property
    def MIDDLEWARE_CLASSES(self):
        return (
            'django.middleware.gzip.GZipMiddleware',
        ) + super(GZip, self).MIDDLEWARE_CLASSES


class HerokuSettings(HerokuMemcache, GZip, SecureFrameDeny,
                     services.Gunicorn):
    INTERNAL_IPS = ('0.0.0.0',)
    CSRF_COOKIE_DOMAIN = ('.herokuapps.com')
