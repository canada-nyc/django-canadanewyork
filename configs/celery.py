from celery import Celery
from django.conf import settings  # noqa

app = Celery('configs')

# Using a string here means the worker will not have to
# pickle the object when using Windows.
app.config_from_object('django.conf:settings')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)
app.conf.update(
    CELERY_ACCEPT_CONTENT=['pickle']
)
