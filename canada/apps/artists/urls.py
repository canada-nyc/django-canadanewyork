from django.conf.urls.defaults import patterns, url
from django.views.generic import list_detail

from .models import *
from .views import *

artist_list_info = {
                        'queryset': Artist.objects.filter(),
                        'template_name': 'artists/list.html',
                        'template_object_name': 'artists',
                        }

urlpatterns = patterns('',
    url(r'^$', list_detail.object_list, artist_list_info, name='artist-index'),
    url(r'^(?P<slug>[-\w]+)/$', single, name='artist-single'),
    )
