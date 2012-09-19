from django.conf.urls.defaults import patterns, url

from .views import InfoDetail


urlpatterns = patterns('',
    url(r'^contact/$', InfoDetail.as_view()),
)
