import os

from django.db import models
from django.core.urlresolvers import reverse
from django.core.exceptions import ValidationError

import caching.base
import url_tracker

from ..artists.models import Artist
from ..exhibitions.models import Exhibition
from libs.slugify.fields import SlugifyField


class Press(caching.base.CachingMixin, url_tracker.URLTrackingMixin, models.Model):
    def file_path(instance, filename):
        return os.path.join(instance.get_absolute_url()[1:], 'content', filename)

    title = models.CharField(
        max_length=500,
        blank=True,
        help_text='If this is blank then the exhibition or artist will be used instead. Also when this is displayed on, it will be prefixed by the publisher, if one is set'
    )
    link = models.URLField(null=True, blank=True, verbose_name=u'External link')
    content = models.TextField(blank=True)
    content_file = models.FileField(upload_to=file_path, blank=True, null=True, max_length=500)

    date = models.DateField()

    publisher = models.CharField(max_length=50, blank=True)
    artist = models.ForeignKey(Artist, blank=True, null=True, related_name='press')
    exhibition = models.ForeignKey(Exhibition, blank=True, null=True, related_name='press',)
    slug = SlugifyField(
        populate_from=('date_year', '__unicode__',),
        slug_template=u'{}/{}',
        unique=True
    )

    objects = caching.base.CachingManager()

    class Meta:
        ordering = ['-date']
        verbose_name_plural = "press"

    def __unicode__(self):
        if self.publisher:
            return u'{}: {}'.format(self.publisher, self.full_title)
        return self.full_title

    def clean(self):
        self.title = self.title.strip().title()
        self.content = self.content.strip()
        self.publisher = self.publisher.strip().title()
        if not (self.artist or self.exhibition or self.title):
            raise ValidationError('A press must have either a title or an artist or an exhibition')

    def get_absolute_url(self):
        return reverse('press-detail', kwargs={'slug': self.slug})

    @property
    def date_year(self):
        return self.date.year

    @property
    def full_title(self):
        'for display in template, prepended by publisher'
        if self.title:
            return self.title
        elif self.exhibition:
            return unicode(self.exhibition)
        elif self.artist:
            return unicode(self.artist)
        return ''

url_tracker.track_url_changes_for_model(Press)
