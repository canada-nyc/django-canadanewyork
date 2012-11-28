from django.conf.urls.defaults import patterns, url

from .views import ArtistList, ArtistDetail, ArtistPressDetail

urlpatterns = patterns(
    '',
    url(r'^$', ArtistList.as_view()),
    url(r'^(?P<slug>[-\w]+)/$', ArtistDetail.as_view(), name='artist-detail'),
    url(r'^(?P<slug>[-\w]+)/press/$', ArtistPressDetail.as_view(),
        name='artist-press-list'),)
