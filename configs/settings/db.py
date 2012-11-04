import dj_database_url

from .django import RelPath


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
    DATABASES = {'default': dj_database_url.config(default='postgres://localhost')}
