from django.conf.urls import patterns, url

from .views import ArtistList, ArtistDetail, ArtistPressList, ArtistResume, ArtistExhibitionList


urlpatterns = patterns(
    '',
    url(r'^$', ArtistList.as_view(), name='artist-list'),
    url(r'^(?P<slug>[-\w]+)/$', ArtistDetail.as_view(), name='artist-detail'),
    url(r'^(?P<slug>[-\w]+)/press/$', ArtistPressList.as_view(), name='artist-press-list'),
    url(r'^(?P<slug>[-\w]+)/exhibitions/$', ArtistExhibitionList.as_view(), name='artist-exhibition-list'),
    url(r'^(?P<slug>[-\w]+)/resume/$', ArtistResume.as_view(), name='artist-resume')
)
