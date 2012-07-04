from django.conf.urls.defaults import patterns, include, url
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns


admin.autodiscover()

urlpatterns = patterns('canada',
                       url(r'^$',
                           'views.frontpage_exhibition',
                           name='frontpage'),
                       url(r'^artists/', include('canada.artists.urls')),
                       url(r'^updates/', include('canada.updates.urls')),
                       url(r'^exhibitions/',
                           include('canada.exhibitions.urls')),
                       url(r'^press/', include('canada.press.urls')),
                       url(r'^contact/$', 'bulkmail.views.bulkmail_contact'),
                       url(r'^admin/bulkmail/',
                           include('canada.bulkmail.urls')),
                       url(r'^feed/$', 'feeds.AllEntriesFeed'),
                       )

urlpatterns += patterns('',
                       url(r'^grappelli/', include('grappelli.urls')),
                       url(r'^admin/', include(admin.site.urls)),
                       )

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += staticfiles_urlpatterns()
