from django.conf.urls.defaults import patterns, url
from django.contrib.auth.decorators import login_required

from .views import InfoDetail


urlpatterns = patterns('',
    url(r'^contact/$', InfoDetail.as_view()),
    url(r'^admin/info/preview/(?P<pk>\d+)$',
        login_required(InfoDetail.as_view()),
        name='info-detail'),
)
