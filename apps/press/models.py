import os

from django.db import models
from django.core.urlresolvers import reverse
from django.core.exceptions import ValidationError

import dumper
import url_tracker

from ..artists.models import Artist
from ..exhibitions.models import Exhibition
from libs.slugify.fields import SlugifyField


SLUG_FIELD_NAMES = ("publisher", "title", "artist", "exhibition")


class Press(url_tracker.URLTrackingMixin, models.Model):
    def file_path(instance, filename):
        return os.path.join(instance.get_absolute_url()[1:], 'content', filename)

    title = models.CharField(
        max_length=500,
        blank=True,
    )

    content = models.TextField(blank=True)
    content_file = models.FileField(upload_to=file_path, blank=True, null=True, max_length=500)

    date = models.DateField(
        verbose_name='Precise Date',
        help_text='Used for ordering'
    )
    date_text = models.CharField(
        verbose_name='Imprecise Date',
        max_length=500,
        blank=True,
        help_text="If set, will display <strong>instead of</strong> the precise date."
    )

    publisher = models.CharField(max_length=50, blank=True)
    author_first_name = models.CharField(max_length=50, blank=True)
    author_last_name = models.CharField(max_length=50, blank=True)
    pages_range = models.CharField(max_length=50, blank=True)

    artist = models.ForeignKey(Artist, blank=True, null=True, related_name='press')
    exhibition = models.ForeignKey(Exhibition, blank=True, null=True, related_name='press',)

    slug = SlugifyField(
        populate_from=('date_year', 'slug_title',),
        slug_template=u'{}/{}',
        unique=True
    )

    class Meta:
        ordering = ['-date']
        verbose_name_plural = "press"
        unique_together = SLUG_FIELD_NAMES

    def __unicode__(self):
        return self.title

    @property
    def _slug_field_values(self):
        values = [getattr(self, field_name) for field_name in SLUG_FIELD_NAMES]
        return filter(None, values)


    def clean(self):
        if not any(self._slug_field_values):
            raise ValidationError('At least one of the following must be filled in: ' + str(SLUG_FIELD_NAMES))

    def get_absolute_url(self):
        return reverse('press-detail', kwargs={'slug': self.slug})

    def get_content_url(self):
        if self.content_file:
            return self.content_file.url
        if self.content:
            return self.get_absolute_url()

    @property
    def slug_title(self):
        return '-'.join(map(str, self._slug_field_values))

    @property
    def date_year(self):
        return self.date.year

    def dependent_paths(self):
        yield self.get_absolute_url()
        if self.artist:
            yield self.artist.get_absolute_url()
            yield reverse('artist-press-list', kwargs={'slug': self.artist.slug})
        if self.exhibition:
            yield self.exhibition.get_absolute_url()
            yield reverse('exhibition-press-list', kwargs={'slug': self.exhibition.slug})

url_tracker.track_url_changes_for_model(Press)
dumper.register(Press)
