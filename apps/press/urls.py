from django.conf.urls.defaults import patterns, url

from .views import PressDetail


urlpatterns = patterns(
    '',
    url(r'^(?P<year>\d{4})/(?P<slug>[-\w]+)', PressDetail.as_view(),
        name='press-detail'),
)
