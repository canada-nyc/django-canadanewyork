from django.conf import settings
from django.conf.urls import include, url
from django.contrib import admin
from django.contrib.sitemaps.views import sitemap
from django.views.static import serve

from .sitemaps import sitemaps

from apps.exhibitions.views import ExhibitionCurrent
from apps.custompages.views import CustomPageDetail


admin.autodiscover()

urlpatterns = [
    url(r'^sitemap\.xml$', sitemap, {'sitemaps': sitemaps}),

    url(r'^$', ExhibitionCurrent.as_view(), name='exhibition-current'),
    url(r'^artists/', include('apps.artists.urls')),
    url(r'^updates/', include('apps.updates.urls')),
    url(r'^exhibitions/', include('apps.exhibitions.urls')),
    url(r'^press/', include('apps.press.urls')),
    url(r'^books/', include('apps.books.urls')),
    url(r'^contact/$', CustomPageDetail.as_view(), name='contact'),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^autocomplete/', include('autocomplete_light.urls')),
]


if 'django_rq' in settings.INSTALLED_APPS:
    urlpatterns += [
        url(r'^admin/django-rq/', include('django_rq.urls')),
    ]


if settings.DEFAULT_FILE_STORAGE == 'django.core.files.storage.FileSystemStorage':
    urlpatterns += [
        url(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
    ]
