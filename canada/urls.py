from django.conf.urls.defaults import patterns, include, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf import settings
from django.contrib import admin

from canada.bulkmail.views import bulkmail_contact
from canada.feeds import AllEntriesFeed
from canada.views import TextView
from canada import settings

admin.autodiscover()

urlpatterns = patterns('',
                        url(r'^$', include('canada.frontpage.urls')),
                        url(r'^exhibitions/', include('canada.exhibitions.urls')),
                        url(r'^artists/', include('canada.artists.urls')),
                        url(r'^updates/', include('canada.updates.urls')),
                        url(r'^press/', include('canada.press.urls')),
                        url(r'^search/', include('canada.search.urls')),
                        url(r'^contact/$', bulkmail_contact),

                        url(r'^admin/bulkmail/', include('canada.bulkmail.urls')),

                        url(r'^grappelli/', include('grappelli.urls')),
                        url(r'^admin/', include(admin.site.urls)),

                        url(r'^feed/$', AllEntriesFeed()),

                        url(r'^robots\.txt$', TextView.as_view(template_name="robots.txt")),
                        url(r'^humans\.txt$', TextView.as_view(template_name="humans.txt")),

)

urlpatterns += staticfiles_urlpatterns()

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
if settings.DEBUG:
    #  uploaded media files (images)
    urlpatterns += patterns('',
        (r'^media/(?P<path>.*)$', 'django.views.static.serve', {
        'document_root': settings.MEDIA_ROOT}))
