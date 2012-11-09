from .django import RelPath
try:
    import dj_database_url
except ImportError:
    dj_database_url = lambda _:_


class SQLite(RelPath):
    @property
    def DATABASES(self):
        db = {
            'default': {
                'ENGINE': 'django.db.backends.sqlite3',
                'NAME': super(SQLite, self).rel_path('tmp/sqlite.db'),
                'USER': '',
                'PASSWORD': '',
                'HOST': '',
                'PORT': '',
            }
        }
        return db


class Postgres(RelPath):
    import dj_database_url
    DATABASES = {'default': dj_database_url.config(default='postgres://localhost')}
