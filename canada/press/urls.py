from django.conf.urls.defaults import patterns, include, url
from canada.press.models import *
from django.views.generic import list_detail
press_list_info = {
                        'queryset': Press.objects.filter(),
                        'template_name': 'press/list.html',
                        'template_object_name':'press',
                        }

urlpatterns = patterns( '',
                    url( r'^$', list_detail.object_list, press_list_info, name='press-index'),
                    url(r'^(?P<year>\d{4})/(?P<title>[-\w]+)', 'press.views.single' , name = 'press-single' ),
                    )