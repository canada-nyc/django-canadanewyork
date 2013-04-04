import os

import url_tracker

from django.db import models
from django.core.urlresolvers import reverse

from ..artists.models import Artist
from ..exhibitions.models import Exhibition
from libs.slugify.fields import SlugifyField


class Press(url_tracker.URLTrackingMixin, models.Model):
    def image_path(instance, filename):
        return os.path.join(instance.get_absolute_url()[1:], 'content', filename)

    title = models.CharField(max_length=500)
    link = models.URLField(null=True, blank=True, verbose_name=u'External link')
    content = models.TextField(blank=True)
    content_file = models.FileField(upload_to=image_path, blank=True, null=True, max_length=500)

    date = models.DateField()

    publisher = models.CharField(max_length=50, blank=True)
    author = models.CharField(max_length=60, blank=True)
    artists = models.ManyToManyField(Artist, blank=True, null=True,
                                     related_name='press',)
    exhibition = models.ForeignKey(Exhibition, blank=True, null=True,
                                   related_name='press',)
    slug = SlugifyField(
        populate_from=('get_year', 'publisher', 'title',),
        slug_template=u'{}/{}-{}',
        unique=True
    )

    class Meta:
        ordering = ['-date']
        verbose_name_plural = "press"

    def __unicode__(self):
        if self.publisher:
            return u'{}: {}'.format(self.publisher, self.title)
        return self.title

    def clean(self):

        self.title = self.title.strip().title()
        self.content = self.content.strip()
        self.publisher = self.publisher.strip().title()
        self.author = self.author.strip().title()

    def get_absolute_url(self):
        return reverse('press-detail', kwargs={'slug': self.slug})

    def get_content_file_url(self):
        '''
        For tracking
        '''
        if self.content_file:
            return self.content_file.url

    @property
    def get_year(self):
        '''
        For slug
        '''
        return self.date.year

    url_tracking_methods = [
        'get_absolute_url',
        'get_content_file_url',
    ]

url_tracker.track_url_changes_for_model(Press)
