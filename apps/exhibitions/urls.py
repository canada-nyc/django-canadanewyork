from django.conf.urls.defaults import patterns, url

from .views import ExhibitionDetail, ExhibitionList, ExhibitionPressDetail


urlpatterns = patterns(
    '',
    url(r'^$', ExhibitionList.as_view()),
    url(r'^(?P<year>\d{1,4})/(?P<slug>[-\w]+)/$', ExhibitionDetail.as_view(),
        name='exhibition-detail'),
    url(r'^(?P<year>\d{1,4})/(?P<slug>[-\w]+)/press/$',
        ExhibitionPressDetail.as_view(),
        name='exhibition-press-list'))
