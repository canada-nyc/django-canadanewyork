import socket


if socket.gethostname() == 'Sauls-Macbook.local':
    from settings.local import *
else:
    from settings.remote import *



if DEBUG:
    INSTALLED_APPS += (
        'django_extensions',
        'debug_toolbar',
       )
    MIDDLEWARE_CLASSES = add_to_middleware(MIDDLEWARE_CLASSES, 'debug_toolbar.middleware.DebugToolbarMiddleware')
    TEMPLATE_CONTEXT_PROCESSORS += ('django.core.context_processors.request',)
TEMPLATE_DEBUG = DEBUG
