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
            'apps.artists',
            'apps.exhibitions',
            'apps.press',
            'apps.updates',
            'apps.bulkmail',
            'apps.updates',
            'apps.frontpage',
            'apps.info',
            'apps.common',
            'apps.model_redirects',
            'apps.unique_boolean'
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
    CSRF_COOKIE_DOMAIN = 'localhost'


class ProductionSettings(Canada, production.HerokuSettings, services.S3):
    pass
