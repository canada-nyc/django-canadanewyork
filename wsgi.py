from raven.contrib.django.raven_compat.middleware.wsgi import Sentry
import django

application = Sentry(django.core.handlers.wsgi.WSGIHandler())
