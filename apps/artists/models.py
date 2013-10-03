from django.db import models
from django.db.models import Q
from django.db.models.loading import get_model
from django.core.urlresolvers import reverse

import url_tracker
import dumper
import simpleimages.trackers

from libs.slugify.fields import SlugifyField
from apps.photos.models import ArtworkPhoto


class VisibleManager(models.Manager):
    def get_query_set(self):
        return super(VisibleManager, self).get_query_set().filter(visible=True)


class Artist(url_tracker.URLTrackingMixin, models.Model):

    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    resume = models.TextField(blank=True)
    slug = SlugifyField(populate_from=('first_name', 'last_name'))
    visible = models.BooleanField(
        default=False,
        help_text="Whether it appears in the artists list, and has an artist page")

    objects = models.Manager()
    in_gallery = VisibleManager()

    class Meta:
        ordering = ['-visible', 'last_name', 'first_name']
        unique_together = ("first_name", "last_name")

    def __unicode__(self):
        return ' '.join([self.first_name, self.last_name])

    @staticmethod
    def autocomplete_search_fields():
        return ("first_name__icontains", "last_name__icontains",)

    def clean(self):
        self.first_name = self.first_name.strip().title()
        self.last_name = self.last_name.strip().title()
        self.resume = self.resume.strip()

    def get_absolute_url(self):
        return reverse('artist-detail', kwargs={'slug': self.slug})

    @property
    def all_press(self):
        return get_model('press', 'Press').objects.filter(
            Q(artist=self) | Q(exhibition__artists__in=[self])
        )

    def dependent_paths(self):
        yield reverse('artist-list')
        yield self.get_absolute_url()
        yield reverse('artist-resume', kwargs={'slug': self.slug})
        yield reverse('artist-press-list', kwargs={'slug': self.slug})
        yield reverse('artist-exhibition-list', kwargs={'slug': self.slug})
        for exhibition in self.exhibitions.all():
            yield exhibition.get_absolute_url()


class ArtistPhoto(ArtworkPhoto):
    content_object = models.ForeignKey(Artist, related_name='photos')


url_tracker.track_url_changes_for_model(Artist)
dumper.register(Artist)
dumper.register(ArtistPhoto)
simpleimages.trackers.track_model(ArtistPhoto)
