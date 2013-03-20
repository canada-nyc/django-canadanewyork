from django.conf.urls import patterns, url

from .views import InfoDisplay


urlpatterns = patterns(
    '',
    url(r'^contact/$', InfoDisplay.as_view()),
)
