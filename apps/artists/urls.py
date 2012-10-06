from django.conf.urls.defaults import patterns, url
from django.views.generic import ListView, DetailView

from .models import Artist


urlpatterns = patterns(
    '',
    url(r'^$', ListView.as_view(queryset=Artist.in_gallery.all())),
    url(r'^(?P<slug>[-\w]+)/$',
        DetailView.as_view(queryset=Artist.in_gallery.all()),
        name='artist-detail'),
    url(r'^(?P<slug>[-\w]+)/press/$',
        DetailView.as_view(queryset=Artist.in_gallery.all(),
                           template_name='press/press_list.html'),
        name='artist-press-list'),)
