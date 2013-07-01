import os

from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.contrib.staticfiles.storage import staticfiles_storage
from django.views.generic import RedirectView
from django.conf import settings
from django.conf.urls.static import static
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
    url(r'^loaderio-98af061ca817542d668fabd7756e14b7\.txt',
        lambda request: HttpResponse('loaderio-98af061ca817542d668fabd7756e14b7')),
    url(r'^sitemap\.xml$',
        'django.contrib.sitemaps.views.sitemap',
        {'sitemaps': sitemaps}),

    url(r'^$', ExhibitionCurrent.as_view(), name='exhibition-current'),
    url(r'^artists/', include('apps.artists.urls')),
    url(r'^updates/', include('apps.updates.urls')),
    url(r'^exhibitions/', include('apps.exhibitions.urls')),
    url(r'^press/', include('apps.press.urls')),

    url(r'^grappelli/', include('grappelli.urls')),
    url(r'^admin/', include(admin.site.urls)),
)

urlpatterns += patterns(
    'django.contrib.flatpages.views',
    url(r'^contact/$', 'flatpage', {'url': '/contact/'}, name='contact')
)

loader_io_verification = os.environ.get('LOADER_IO_VERIFICATION', None)
if loader_io_verification:
    urlpatterns += patterns(
        url(
            '^' + loader_io_verification,
            lambda request: HttpResponse(loader_io_verification)
        ),
    )

if settings.DEFAULT_FILE_STORAGE == 'django.core.files.storage.FileSystemStorage':
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
