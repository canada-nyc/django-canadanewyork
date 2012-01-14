from django.conf.urls.defaults import patterns, url
from canada.artists.models import *
from canada.artists.views import *
from django.views.generic import list_detail

artist_list_info = {
                        'queryset': Artist.objects.filter(),
                        'template_name': 'artists/list.html',
                        'template_object_name':'artists',
                        }

urlpatterns = patterns( '',
                    url( r'^$', list_detail.object_list, artist_list_info, name='artist-index'),
                    url( r'^(?P<first_name>[-\w]+)-(?P<last_name>[-\w]+)/$', single, name='artist-single'),
                    )
