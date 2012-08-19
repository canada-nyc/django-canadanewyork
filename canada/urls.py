from django.conf.urls.defaults import patterns, include, url
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from .feeds import AllEntriesFeed


admin.autodiscover()

urlpatterns = patterns('',
    url(r'^', include('canada.apps.frontpage.urls')),
    url(r'^artists/', include('canada.apps.artists.urls')),
    url(r'^updates/', include('canada.apps.updates.urls')),
    url(r'^exhibitions/', include('canada.apps.exhibitions.urls')),
    url(r'^press/', include('canada.apps.press.urls')),
    url(r'^', include('canada.apps.info.urls')),
    url(r'^', include('canada.apps.bulkmail.urls')),

    url(r'^feed/$', AllEntriesFeed),
 )

urlpatterns += patterns('',
   url(r'^grappelli/', include('grappelli.urls')),
   url(r'^admin/', include(admin.site.urls)),
   url(r'^chaining/', include('smart_selects.urls')),
)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                        document_root=settings.MEDIA_ROOT)
    urlpatterns += staticfiles_urlpatterns()
