from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('',
                    url(r'^$', 'frontpage.views.frontpage_exhibition', name='frontpage'),
                   )
