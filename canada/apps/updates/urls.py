from django.conf.urls.defaults import patterns, url

from .views import UpdateListView

urlpatterns = patterns('',
    url(r'^$', UpdateListView.as_view(), name='updates-list'),
    url(r'^\#(?P<slug>[-\w]+)$',
        UpdateListView.as_view(),
        name='update-single'),
   )
