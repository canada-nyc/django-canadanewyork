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
        ('text/less', 'lessc {infile} {outfile}'),
    )

    @property
    def COMPRESS_STORAGE(self):
        return super(Compress, self).STATICFILES_STORAGE

    @property
    def COMPRESS_URL(self):
        bucket = getattr(super(Compress, self), 'AWS_STORAGE_BUCKET_NAME', 0)
        if bucket:
            return 'https://{}.s3.amazonaws.com/'.format(bucket)


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

    @property
    def THUMBNAIL_DEFAULT_STORAGE(self):
        if hasattr(super(Thumbnail, self), 'AWS_STORAGE_BUCKET_NAME'):
            return 'storages.backends.s3boto.S3BotoStorage'
        return 'easy_thumbnails.storage.ThumbnailFileSystemStorage'


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
        return self.NAME

    @property
    def ADMIN_MEDIA_PREFIX(self):
        return super(Grappelli, self).STATIC_URL + "grappelli/"


class Markdown(object):

    @property
    def INSTALLED_APPS(self):
        return (
            'markdown_deux',
        ) + super(Markdown, self).INSTALLED_APPS

    MARKDOWN_DEUX_STYLES = {
        "default": {
            "safe_mode": "escape",
        },
    }


class Sekizai(object):
    @property
    def INSTALLED_APPS(self):
        return (
            'sekizai',
        ) + super(Sekizai, self).INSTALLED_APPS

    @property
    def TEMPLATE_CONTEXT_PROCESSORS(self):
        return (
            'sekizai.context_processors.sekizai',
        ) + super(Sekizai, self).TEMPLATE_CONTEXT_PROCESSORS
