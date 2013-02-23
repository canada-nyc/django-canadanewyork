from django.conf.urls.defaults import patterns, url

from .views import PressDetail


urlpatterns = patterns(
    '',
    url(r'^(?P<slug>\d{4}/[-\w]+)', PressDetail.as_view(),
        name='press-detail'),
)
