from . import django


class Compress(django.Static):

    @property
    def INSTALLED_APPS(self):
        return (
            'compressor',
        ) + super(Compress, self).INSTALLED_APPS

    @property
    def STATICFILES_FINDERS(self):
        return (
            'compressor.finders.CompressorFinder',
        ) + super(Compress, self).STATICFILES_FINDERS

    COMPRESS_ENABLED = True

    COMPRESS_CSS_FILTERS = [
        'compressor.filters.css_default.CssAbsoluteFilter',
        'compressor.filters.cssmin.CSSMinFilter'
    ]

    COMPRESS_PRECOMPILERS = (
        ('text/less', 'lessc -x {infile} {outfile}'),
    )

    @property
    def COMPRESS_STORAGE(self):
        return super(Compress, self).STATICFILES_STORAGE

    @property
    def COMPRESS_URL(self):
        if super(Compress, self).AWS_STORAGE_BUCKET_NAME:
            return 'https://{}.s3.amazonaws.com/'.format(super(Compress, self).AWS_STORAGE_BUCKET_NAME)


class South(object):

    @property
    def INSTALLED_APPS(self):
        return (
            'south',
        ) + super(South, self).INSTALLED_APPS


class Thumbnail(django.Media):

    @property
    def INSTALLED_APPS(self):
        return (
            'sorl.thumbnail',
        ) + super(Thumbnail, self).INSTALLED_APPS


class SmartSelects(django.Admin):

    @property
    def INSTALLED_APPS(self):
        return (
            'smart_selects',
        ) + super(SmartSelects, self).INSTALLED_APPS


class TwitterBootstrap(object):

    @property
    def INSTALLED_APPS(self):
        return (
            'bootstrapform',
        ) + super(TwitterBootstrap, self).INSTALLED_APPS


class Grappelli(django.Admin):
    @property
    def INSTALLED_APPS(self):
        return (
            'grappelli',
        ) + super(Grappelli, self).INSTALLED_APPS

    @property
    def GRAPPELLI_ADMIN_TITLE(self):
        return super(Grappelli, self).NAME

    @property
    def ADMIN_MEDIA_PREFIX(self):
        return super(Grappelli, self).STATIC_URL + "grappelli/"


class Markdown(object):

    @property
    def INSTALLED_APPS(self):
        return (
            'grappelli',
        ) + super(Markdown, self).INSTALLED_APPS

    MARKDOWN_DEUX_STYLES = {
            "default": {
            "safe_mode": "escape",
        },
    }
