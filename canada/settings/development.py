from .django import RelPath


class SQLite(RelPath):

    @property
    def DATABASES(self):
        return {
            'default': {
                    'ENGINE': 'django.db.backends.sqlite3',
                    'NAME':  super(SQLite, self).rel_path('../sqlite.db'),
                    'USER': '',
                    'PASSWORD': '',
                    'HOST': '',
                    'PORT': '',
                    }
            }


class DebugToolbar(object):
    @property
    def MIDDLEWARE_CLASSES(self):
        return super(DebugToolbar, self).MIDDLEWARE_CLASSES + (
            'debug_toolbar.middleware.DebugToolbarMiddleware',
        )

    @property
    def INSTALLED_APPS(self):
        return (
            'debug_toolbar',
        ) + super(DebugToolbar, self).INSTALLED_APPS

    DEBUG_TOOLBAR_CONFIG = {
        'INTERCEPT_REDIRECTS': False,
    }


class PDB(object):
    @property
    def MIDDLEWARE_CLASSES(self):
        return super(PDB, self).MIDDLEWARE_CLASSES + (
            'django_pdb.middleware.PdbMiddleware',
        )

    @property
    def INSTALLED_APPS(self):
        return (
            'django_pdb',
        ) + super(PDB, self).INSTALLED_APPS


class Local(SQLite):
    INTERNAL_IPS = ('127.0.0.1',)
    CSRF_COOKIE_DOMAIN = 'localhost'


class Debug(DebugToolbar, PDB):
    DEBUG = True
