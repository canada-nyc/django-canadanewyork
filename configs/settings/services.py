import os


class Gunicorn(object):
    @property
    def INSTALLED_APPS(self):
        return (
            'gunicorn',
        ) + super(Gunicorn, self).INSTALLED_APPS


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
    AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID')
    AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY')
    AWS_STORAGE_BUCKET_NAME = os.environ.get('AWS_STORAGE_BUCKET_NAME')
    STATICFILES_STORAGE = DEFAULT_FILE_STORAGE
