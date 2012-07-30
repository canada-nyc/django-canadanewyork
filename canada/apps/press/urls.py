from django.conf.urls.defaults import patterns, url
from django.views.generic import ListView, DetailView

from .models import Press, Publisher
from .views import PressDetail


urlpatterns = patterns('',
    url(r'^$', ListView.as_view(model=Press)),
    url(r'^(?P<year>\d{4})/(?P<slug>[-\w]+)', PressDetail.as_view(),
        name='press-detail'),
    url(r'^publisher/(?P<slug>[-\w]+)', DetailView.as_view(model=Publisher),
        name='publisher-detail'),
)
