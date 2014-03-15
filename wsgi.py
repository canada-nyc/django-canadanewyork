from django.core.handlers.wsgi import WSGIHandler

from whitenoise.django import DjangoWhiteNoise
from raven.contrib.django.raven_compat.middleware.wsgi import Sentry

application = DjangoWhiteNoise(WSGIHandler())
application = Sentry(application)
