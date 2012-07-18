from django.conf.urls.defaults import patterns, include, url
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from .apps.artists.urls import urlpatterns as artists_urls
from .apps.updates.urls import urlpatterns as updates_urls
from .apps.exhibitions.urls import urlpatterns as exhibitions_urls
from .apps.press.urls import urlpatterns as press_urls
from .apps.bulkmail.urls import urlpatterns as bulkmail_urls
from .apps.frontpage.urls import urlpatterns as frontpage_urls


from .feeds import AllEntriesFeed


admin.autodiscover()

urlpatterns = patterns('',
    url(r'^', include(frontpage_urls)),
    url(r'^artists/', include(artists_urls)),
    url(r'^updates/', include(updates_urls)),
    url(r'^exhibitions/', include(exhibitions_urls)),
    url(r'^press/', include(press_urls)),
#    url(r'^contact/$', bulkmail_contact),
    url(r'^admin/bulkmail/preview/', include(bulkmail_urls)),

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
