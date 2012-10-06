import imp
import os


class RelPath(object):
    @property
    def SITE_ROOT(self):
        return os.path.dirname(imp.find_module('manage')[1])

    def rel_path(self, relative_path):
        '''
        given any path relative to the `SITE_ROOT`, returns the full path
        '''
        return os.path.normpath(os.path.join(self.SITE_ROOT,
                                             relative_path))


class DjangoDefault(object):
    SITE_ID = 1
    SECRET_KEY = os.environ.get('SECRET_KEY', '*YSHFUIH&GAHJBJCZKCY)P#R')
    WSGI_APPLICATION = 'manage.application'
    DATE_FORMAT = 'F j, Y'

    @property
    def TEMPLATE_DEBUG(self):
        return super(DjangoDefault, self).DEBUG

    @property
    def TEMPLATE_DIRS(self):
        return (super(DjangoDefault, self).rel_path('templates'), )

    @property
    def ROOT_URLCONF(self):
        return self.NAME + '.urls'


class Media(object):
    MEDIA_URL = '/media/'

    @property
    def MEDIA_ROOT(self):
        return super(Media, self).rel_path('tmp/media/')


class Static(object):
    STATIC_URL = '/static/'

    @property
    def INSTALLED_APPS(self):
        return super(Static, self).INSTALLED_APPS + ('django.contrib.staticfiles',)

    @property
    def STATIC_ROOT(self):
        return super(Static, self).rel_path('tmp/static/')

    @property
    def STATICFILES_DIRS(self):
        return (
            (self.NAME,
             super(Static, self).rel_path('static')),
        )


class Admin(Static):

    @property
    def INSTALLED_APPS(self):
        return (
            'django.contrib.admin',
            'django.contrib.auth',
            'django.contrib.contenttypes',
            'django.contrib.sessions',
            'django.contrib.messages',
        ) + super(Admin, self).INSTALLED_APPS


class Email(object):
    EMAIL_HOST = "smtp.gmail.com"
    EMAIL_PORT = 587
    EMAIL_HOST_USER = "s.shanabrook@gmail.com"
    EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD', '')
    EMAIL_USE_TLS = True

    @property
    def INSTALLED_APPS(self):
        return (
            'django.contrib.sites',
        ) + super(Email, self).INSTALLED_APPS
