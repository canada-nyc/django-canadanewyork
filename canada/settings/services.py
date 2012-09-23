import os


class HerokuDB(object):
    import dj_database_url
    DATABASES = {'default': dj_database_url.config(default='postgres://localhost')}


class HerokuMemcache(object):
    from memcacheify import memcacheify

    CACHES = memcacheify()


class Gunicorn(object):
    @property
    def INSTALLED_APPS(self):
        return (
            'gunicorn',
        ) + super(Gunicorn, self).INSTALLED_APPS


class Heroku(HerokuDB, HerokuMemcache, Gunicorn):
    INTERNAL_IPS = ('0.0.0.0',)


class RQ(object):

    @property
    def INSTALLED_APPS(self):
        return (
            'django_rq',
        ) + super(RQ, self).INSTALLED_APPS

    RQ_QUEUES = {
        'default': {
            'URL': os.getenv('REDISTOGO_URL', 'redis://localhost:6379'),
            'DB': 0,
        },
    }


class S3(object):
    @property
    def INSTALLED_APPS(self):
        return (
            'storages',
        ) + super(S3, self).INSTALLED_APPS

    DEFAULT_FILE_STORAGE = 'storages.backends.s3boto.S3BotoStorage'
    AWS_ACCESS_KEY_ID = os.environ['AWS_ACCESS_KEY_ID']
    AWS_SECRET_ACCESS_KEY = os.environ['AWS_SECRET_ACCESS_KEY']
    AWS_STORAGE_BUCKET_NAME = os.environ['AWS_STORAGE_BUCKET_NAME']
    STATICFILES_STORAGE = DEFAULT_FILE_STORAGE
