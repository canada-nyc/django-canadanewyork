from raven.contrib.django.raven_compat.middleware.wsgi import Sentry
from django.core.handlers.wsgi import WSGIHandler

application = Sentry(WSGIHandler())
