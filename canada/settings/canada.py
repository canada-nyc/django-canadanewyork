from . import django, apps, development, production, testing

from configurations import Settings


class Canada(django.DjangoDefault,
             django.Email,
             apps.Grappelli,
             apps.Markdown,
             apps.SmartSelects,
             apps.Thumbnail,
             apps.TwitterBootstrap,
             apps.South,
             apps.Compress,
             Settings):
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
                    development.Local,
                    development.Debug,
                    testing.Testing):
    pass

"""
class HerokuSettings(Canada,
                     production.SecureFrameDeny,
                     production.GZip,
                     services.S3,
                     services.RQ,
                     services.Heroku):
    pass
"""
