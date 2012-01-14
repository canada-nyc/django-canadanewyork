from django.conf.urls.defaults import patterns, url
from canada.exhibitions.models import Exhibition
from django.views.generic import list_detail

exhibitions_list_info = {
    'queryset': Exhibition.objects.all(),
    'template_name': 'exhibitions/list.html',
    'template_object_name': 'exhibitions',
    }

urlpatterns = patterns('',
                       url(r'^$', list_detail.object_list, exhibitions_list_info, name='exhibition-index'),
                       url(r'^(?P<year>\d{4})/(?P<slug>[-\w]+)', 'canada.exhibitions.views.single',
                           name='exhibition-single'),
                       )
