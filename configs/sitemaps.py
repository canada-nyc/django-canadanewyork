from django.contrib.sitemaps import GenericSitemap

from apps.artists.models import Artist
from apps.exhibitions.models import Exhibition
from apps.press.models import Press
from apps.updates.models import Update

sitemaps = {
    'artists': GenericSitemap(
        info_dict={
            'queryset': Artist.in_gallery.all(),
        },
        priority=0.9,
        changefreq='monthly',
    ),
    'exhibitions': GenericSitemap(
        info_dict={
            'queryset': Exhibition.objects.all(),
            'date_field': 'start_date',
        },
        priority=0.7,
        changefreq='never',
    ),
    'press': GenericSitemap(
        info_dict={
            'queryset': Press.objects.all(),
            'date_field': 'date',
        },
        priority=0.5,
        changefreq='never',
    ),
    'updates': GenericSitemap(
        info_dict={
            'queryset': Update.objects.all(),
            'date_field': 'post_date',
        },
        priority=0.3,
        changefreq='never',
    ),
}
