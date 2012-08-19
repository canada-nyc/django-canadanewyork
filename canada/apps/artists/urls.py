from django.conf.urls.defaults import patterns, url
from django.views.generic import ListView

from .models import Artist
from .views import ArtistDetailPress


urlpatterns = patterns('',
    url(r'^$', ListView.as_view(queryset=Artist.in_gallery.all()),
        name='artist-list'),
    url(r'^(?P<slug>[-\w]+)/(?P<press>(press)|)$',
        ArtistDetailPress.as_view(),
        name='artist-detail'),
    )
