from . import django, apps, development, production, testing, services, db

from configurations import Settings


class Canada(django.DjangoDefault,
             django.Email,
             django.Redirects,
             production.GZip,
             production.SecureFrameDeny,
             production.CSRF,
             services.RQ,
             apps.Grappelli,
             apps.Markdown,
             apps.SmartSelects,
             apps.Thumbnail,
             apps.TwitterBootstrap,
             apps.South,
             apps.Compress):
    CANADA_IMAGE_SIZE = 'x300'
    CANADA_FRONTPAGE_IMAGE_SIZE = 'x400'
    CANADA_ADMIN_THUMBS_SIZE = 'x60'

    NAME = 'canada'

    @property
    def INSTALLED_APPS(self):
        return (
            'apps.artists',
            'apps.exhibitions',
            'apps.press',
            'apps.updates',
            'apps.bulkmail',
            'apps.updates',
            'apps.frontpage',
            'apps.info',
            'apps.common',
            'tests.apps.content_redirects'
        ) + super(Canada, self).INSTALLED_APPS

    @property
    def TEMPLATE_CONTEXT_PROCESSORS(self):
        return (
            'apps.common.context_processors.image_size',
        ) + super(Canada, self).TEMPLATE_CONTEXT_PROCESSORS


class LocalSettings(Canada,
                    db.SQLite,
                    development.Debug,
                    testing.Testing,
                    Settings):
    INTERNAL_IPS = ('127.0.0.1',)


class ProductionSettings(Canada,
                         db.Postgres,
                         production.HerokuMemcache,
                         services.Gunicorn,
                         services.S3,
                         Settings):
    INTERNAL_IPS = ('0.0.0.0',)


class TravisSetttings(Canada,
                      db.Postgres,
                      production.HerokuMemcache,
                      services.Gunicorn,
                      Settings):
    pass
