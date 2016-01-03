from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.BookList.as_view(), name='book-list'),
    url(r'^(?P<pk>\d+)/$', views.BookDetail.as_view(),
        name='book-detail'),
]
