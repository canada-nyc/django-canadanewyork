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


class Debug(DebugToolbar, PDB):
    DEBUG = True
