from django.conf.urls import url

from .views import PressDetail


urlpatterns = [
    url(r'^(?P<slug>\d{4}/[-\w]*)', PressDetail.as_view(), name='press-detail'),
]
