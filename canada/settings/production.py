class SecureFrameDeny(object):
    SECURE_FRAME_DENY = True


class GZip(object):
    @property
    def MIDDLEWARE_CLASSES(self):
        return (
            'django.middleware.gzip.GZipMiddleware',
        ) + super(GZip, self).MIDDLEWARE_CLASSES
