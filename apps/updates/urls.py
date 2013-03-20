from django.conf.urls import patterns, url

from .views import UpdateList

urlpatterns = patterns(
    '',
    url(r'^$', UpdateList.as_view()),
    url(r'^\#(?P<pk>[-\w]+)$', UpdateList.as_view(),
        name='update-single'),
)
