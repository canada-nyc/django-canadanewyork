import os


def rel_path(ending):
    return os.path.abspath(os.path.join(os.path.dirname(__file__), str(ending)))

DATABASES = {
    'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME':  rel_path('../sqlite.db'),
            'USER': '',
            'PASSWORD': '',
            'HOST': '',
            'PORT': '',
            }
    }
