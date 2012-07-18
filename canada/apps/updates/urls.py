from django.conf.urls.defaults import patterns, url
from django.views.generic import ListView

from .models import Update

urlpatterns = patterns('',
    url(r'^$', ListView.as_view(model=Update)),
    url(r'^\#(?P<slug>[-\w]+)$', ListView.as_view(model=Update),
        name='update-single'),
)
