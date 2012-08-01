from django.conf.urls.defaults import patterns, url
from django.views.generic import DetailView, ListView

from .models import Artist


urlpatterns = patterns('',
    url(r'^$', ListView.as_view(queryset=Artist.in_gallery.all()),
        name='artist-list'),
    url(r'^(?P<slug>[-\w]+)/$',
        DetailView.as_view(queryset=Artist.in_gallery.all()),
        name='artist-detail'),
    )
