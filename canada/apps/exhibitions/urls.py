from django.conf.urls.defaults import patterns, url
from django.views.generic import ListView

from .models import Exhibition
from .views import ExhibitionDetail


urlpatterns = patterns('',
    url(r'^$', ListView.as_view(model=Exhibition)),
    url(r'^(?P<year>\d{4})/(?P<slug>[-\w]+)/$', ExhibitionDetail.as_view(),
        name='exhibition-detail'),
    url(r'^(?P<year>\d{4})/(?P<slug>[-\w]+)/press/$',
        ExhibitionDetail.as_view(template_name='press/press_list.html'),
        name='exhibition-press-list'),
)
