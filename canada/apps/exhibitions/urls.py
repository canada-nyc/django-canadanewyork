from django.conf.urls.defaults import patterns, url

from .views import ExhibitionDetail, ExhibitionList


urlpatterns = patterns('',
    url(r'^$', ExhibitionList.as_view()),
    url(r'^(?P<year>\d{4})/(?P<name>[-\w]+)', ExhibitionDetail.as_view(),),
)
