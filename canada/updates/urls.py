from django.conf.urls.defaults import patterns, include, url
from canada.updates.views import UpdateListView

urlpatterns = patterns('',
    url(r'^$', UpdateListView.as_view(), name='updates_list'),
    url( r'^\#(?P<year>\d{4})\-(?P<slug>[-\w]+)$', UpdateListView.as_view(), name='update-single'),
    )
