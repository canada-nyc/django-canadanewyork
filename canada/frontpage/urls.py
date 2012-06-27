from django.conf.urls.defaults import patterns, url

from .views import frontpage_exhibition

urlpatterns = patterns('',
                    url(r'^$', frontpage_exhibition, name='frontpage'),
                   )
