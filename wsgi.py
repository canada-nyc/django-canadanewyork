from raven.contrib.django.raven_compat.middleware.wsgi import Sentry
from django.core.handlers.wsgi import WSGIHandler
from dj_static import Cling

application = Cling(Sentry(WSGIHandler()))
