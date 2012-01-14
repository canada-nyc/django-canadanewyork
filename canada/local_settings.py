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
BROKER_HOST = "127.0.0.1"
BROKER_PORT = 5672
BROKER_VHOST = "/"
BROKER_USER = "guest"
BROKER_PASSWORD = "guest"

MEDIA_ROOT = rel_path("../media")
STATIC_ROOT = rel_path("../static")
