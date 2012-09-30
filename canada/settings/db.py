from .django import RelPath


class SQLite(RelPath):
    @property
    def DATABASES(self):
        db = {
            'default': {
                'ENGINE': 'django.db.backends.sqlite3',
                'NAME': super(SQLite, self).rel_path('../sqlite.db'),
                'USER': '',
                'PASSWORD': '',
                'HOST': '',
                'PORT': '',
            }
        }
        return db


class HerokuDB(object):
    try:
        import dj_database_url
    except:
        pass
    else:
        DATABASES = {'default': dj_database_url.config(default='postgres://localhost')}
