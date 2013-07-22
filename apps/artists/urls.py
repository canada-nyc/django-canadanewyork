from django.conf.urls import patterns, url

from . import views

urlpatterns = patterns(
    '',
    url(r'^$', views.ArtistList.as_view(), name='artist-list'),
    url(r'^(?P<slug>[-\w]+)/$', views.ArtistDetail.as_view(), name='artist-detail'),
    url(r'^(?P<slug>[-\w]+)/press/$', views.ArtistPressList.as_view(), name='artist-press-list'),
    url(r'^(?P<slug>[-\w]+)/exhibitions/$', views.ArtistExhibitionList.as_view(), name='artist-exhibition-list'),
    url(r'^(?P<slug>[-\w]+)/books/$', views.ArtistBookList.as_view(), name='artist-book-list'),
    url(r'^(?P<slug>[-\w]+)/resume/$', views.ArtistResume.as_view(), name='artist-resume')
)
