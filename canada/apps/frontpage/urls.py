from django.conf.urls.defaults import patterns, url
from django.contrib.auth.decorators import login_required

from .views import FrontpageDetail


urlpatterns = patterns('',
    url(r'^$', FrontpageDetail.as_view(), name='frontpage'),
    url(r'^admin/frontpage/preview/(?P<pk>\d+)$',
        login_required(FrontpageDetail.as_view()),
        name='frontpage-detail'),
)
