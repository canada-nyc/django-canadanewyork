from django.conf.urls.defaults import patterns, url
from django.contrib.auth.decorators import login_required

from .views import ContactDetail


urlpatterns = patterns('',
    url(r'^contact/$', ContactDetail.as_view()),
    url(r'^admin/contact/preview/(?P<pk>\d+)$',
        login_required(ContactDetail.as_view()),
        name='contact-detail'),
)
