from django.conf.urls.defaults import patterns, include, url
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns


admin.autodiscover()

urlpatterns = patterns(
    '',
    url(r'^', include('apps.frontpage.urls')),
    url(r'^artists/', include('apps.artists.urls')),
    url(r'^updates/', include('apps.updates.urls')),
    url(r'^exhibitions/', include('apps.exhibitions.urls')),
    url(r'^press/', include('apps.press.urls')),
    url(r'^', include('apps.info.urls')),
    url(r'^', include('apps.bulkmail.urls')),

urlpatterns += patterns(
    '',
    url(r'^grappelli/', include('grappelli.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^chaining/', include('smart_selects.urls')),)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
    urlpatterns += staticfiles_urlpatterns()
