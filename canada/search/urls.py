from django.conf.urls.defaults import patterns, url
from django.views.generic import TemplateView

urlpatterns = patterns( '',
                    url( r'^$', 'search.views.form'),
                    )
