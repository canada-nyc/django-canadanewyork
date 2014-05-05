from django.core.wsgi import get_wsgi_application

from whitenoise.django import DjangoWhiteNoise
from raven.contrib.django.raven_compat.middleware.wsgi import Sentry

application = DjangoWhiteNoise(get_wsgi_application())
application = Sentry(application)
