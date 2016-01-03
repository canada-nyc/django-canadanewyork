from django.conf.urls import url

from .views import UpdateList

urlpatterns = [
    url(r'^$', UpdateList.as_view(), name='update-list'),
    url(r'^\#update_(?P<pk>[-\w]+)$', UpdateList.as_view(),
        name='update-detail'),
]
