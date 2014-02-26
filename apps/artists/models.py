import os

from django.db import models
from django.db.models import Q
from django.db.models.loading import get_model
from django.core.urlresolvers import reverse

import url_tracker
import dumper
import simpleimages.trackers

from libs.slugify.fields import SlugifyField
from libs.ckeditor.fields import CKEditorField
from apps.photos.models import ArtworkPhoto


class VisibleManager(models.Manager):

    def get_query_set(self):
        return super(VisibleManager, self).get_query_set().filter(visible=True)


class Artist(url_tracker.URLTrackingMixin, models.Model):

    def file_path(instance, filename):
        return os.path.join(
            instance.get_absolute_url()[1:],
            'resume',
            filename)

    date = models
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    resume = CKEditorField(
        blank=True,
        verbose_name='Resume text')
    website = models.URLField(blank=True)
    resume_file = models.FileField(
        upload_to=file_path,
        blank=True,
        null=True,
        max_length=500,
        help_text="Takes preference over resume text")
    slug = SlugifyField(populate_from=('first_name', 'last_name'))
    visible = models.BooleanField(
        default=False,
        help_text="Whether it appears in artists list and has a page")

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

    def get_resume_page_url(self):
        return reverse('artist-resume', kwargs={'slug': self.slug})

    def get_resume_url(self):
        if self.resume_file:
            return self.resume_file.url
        if self.resume:
            return self.get_resume_page_url()

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
