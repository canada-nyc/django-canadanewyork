import os
import re

from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.contrib.staticfiles.storage import staticfiles_storage
from django.views.generic import RedirectView
from django.conf import settings
from django.http import HttpResponse

from .sitemaps import sitemaps

from apps.exhibitions.views import ExhibitionCurrent


admin.autodiscover()

urlpatterns = patterns(
    '',
    url(r'^favicon\.ico$',
        RedirectView.as_view(
            url=staticfiles_storage.url('canada/images/fire_favicon.ico')
        )),
    url(r'^sitemap\.xml$',
        'django.contrib.sitemaps.views.sitemap',
        {'sitemaps': sitemaps}),

    url(r'^$', ExhibitionCurrent.as_view(), name='exhibition-current'),
    url(r'^artists/', include('apps.artists.urls')),
    url(r'^updates/', include('apps.updates.urls')),
    url(r'^exhibitions/', include('apps.exhibitions.urls')),
    url(r'^press/', include('apps.press.urls')),
    url(r'^books/', include('apps.books.urls')),

    url(r'^grappelli/', include('grappelli.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^django-rq/', include('django_rq.urls')),
)

urlpatterns += patterns(
    'django.contrib.flatpages.views',
    url(r'^contact/$', 'flatpage', {'url': '/contact/'}, name='contact')
)


loader_io_verification = os.environ.get('LOADER_IO_VERIFICATION', None)
if loader_io_verification:
    urlpatterns += patterns(
        '',
        url(
            r'^' + re.escape(loader_io_verification) + r'/$',
            lambda request: HttpResponse(loader_io_verification)
        ),
    )

if settings.DEFAULT_FILE_STORAGE == 'django.core.files.storage.FileSystemStorage':
    urlpatterns += patterns(
        '',
        url(r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.STATIC_ROOT}),
        url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
    )
