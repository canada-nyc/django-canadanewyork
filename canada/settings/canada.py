from . import django, apps, development, production, testing, services, db

from configurations import Settings


class Canada(django.DjangoDefault,
             django.Email,
             apps.Grappelli,
             apps.Markdown,
             apps.SmartSelects,
             apps.Thumbnail,
             apps.TwitterBootstrap,
             apps.South,
             services.RQ,
             apps.Compress):
    CANADA_IMAGE_SIZE = 'x300'
    CANADA_FRONTPAGE_IMAGE_SIZE = 'x400'
    CANADA_ADMIN_THUMBS_SIZE = 'x60'

    NAME = 'canada'

    @property
    def INSTALLED_APPS(self):
        return (
            'canada.apps.artists',
            'canada.apps.exhibitions',
            'canada.apps.press',
            'canada.apps.updates',
            'canada.apps.bulkmail',
            'canada.apps.updates',
            'canada.apps.frontpage',
            'canada.apps.info',
            'canada.apps.base'
        ) + super(Canada, self).INSTALLED_APPS

    @property
    def TEMPLATE_CONTEXT_PROCESSORS(self):
        return (
            'canada.apps.base.context_processors.image_size',
        ) + super(Canada, self).TEMPLATE_CONTEXT_PROCESSORS


class LocalSettings(Canada,
                    db.SQLite,
                    development.Debug,
                    testing.Testing,
                    Settings):
    INTERNAL_IPS = ('127.0.0.1',)
    CSRF_COOKIE_DOMAIN = 'localhost'


class HerokuSettings(Canada,
                     production.SecureFrameDeny,
                     production.GZip,
                     services.S3,
                     production.HerokuMemcache,
                     services.Gunicorn):
    INTERNAL_IPS = ('0.0.0.0',)
    CSRF_COOKIE_DOMAIN = ('.herokuapps.com')
