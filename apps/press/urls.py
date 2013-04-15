from django.conf.urls import patterns, url

from .views import PressDetail, PressList


urlpatterns = patterns(
    '',
    url(r'^$', PressList.as_view(), name='press-list'),
    url(r'^(?P<slug>\d{4}/[-\w]*)', PressDetail.as_view(), name='press-detail'),
)
