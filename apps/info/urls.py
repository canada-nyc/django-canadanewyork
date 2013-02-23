from django.conf.urls.defaults import patterns, url

from .views import InfoDisplay


urlpatterns = patterns(
    '',
    url(r'^contact/$', InfoDisplay.as_view()),
)
