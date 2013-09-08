from django.conf.urls import patterns, url

from .views import ExhibitionDetail, ExhibitionList, ExhibitionPressList, ExhibitionPressRelease


urlpatterns = patterns(
    '',
    url(r'^$', ExhibitionList.as_view(), name='exhibition-list'),
    url(r'^(?P<slug>\d{4}/[-\w]+)/$', ExhibitionDetail.as_view(),
        name='exhibition-detail'),
    url(r'^(?P<slug>\d{4}/[-\w]+)/press/$',
        ExhibitionPressList.as_view(),
        name='exhibition-press-list'),
    url(r'^(?P<slug>\d{4}/[-\w]+)/press-release/$',
        ExhibitionPressRelease.as_view(),
        name='exhibition-pressrelease'),
)
