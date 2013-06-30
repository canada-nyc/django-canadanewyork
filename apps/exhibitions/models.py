import os

from django.db import models
from django.core.exceptions import ValidationError
from django.contrib.contenttypes import generic
from django.core.urlresolvers import reverse

import url_tracker

from ..artists.models import Artist
from libs.slugify.fields import SlugifyField
from apps.photos.models import Photo
from libs.unique_boolean.fields import UniqueBooleanField


class Exhibition(url_tracker.URLTrackingMixin, models.Model):

    def image_path(instance, filename):
        return os.path.join(instance.get_absolute_url()[1:], 'press_release_photos', filename)

    name = models.CharField(max_length=1000, unique_for_year='start_date')
    description = models.TextField(blank=True)
    artists = models.ManyToManyField(Artist, related_name='exhibitions',
                                     blank=True, null=True)
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    slug = SlugifyField(
        populate_from=('get_year', 'name',),
        slug_template=u'{}/{}',
        unique=True
    )

    current = UniqueBooleanField(
        help_text="To switch to a different exhibition, activate on another",
        default=True
    )

    press_release_photo = models.ImageField(
        upload_to=image_path,
        help_text='Used if it is the current exhibition, if not specified will use first of the uploaded photos',
        height_field='press_release_photo_height',
        width_field='press_release_photo_width',
        blank=True,
        null=True
    )
    press_release_photo_height = models.PositiveIntegerField(
        null=True,
        blank=True,
        editable=False,
    )
    press_release_photo_width = models.PositiveIntegerField(
        null=True,
        blank=True,
        editable=False,
    )

    photos = generic.GenericRelation(Photo)

    class Meta:
        ordering = ["-start_date"]

    def __unicode__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('exhibition-detail', kwargs={'slug': self.slug})

    def save(self, *args, **kwargs):
        if self.start_date == self.end_date:
            self.end_date = None
        super(Exhibition, self).save(*args, **kwargs)
        return self

    def clean(self):
        if self.end_date and self.start_date > self.end_date:
            raise ValidationError('Start date can not be after end date')

        self.name = self.name.strip()
        self.description = self.description.strip()

    def get_press_release_photo(self):
        if self.press_release_photo:
            return {
                'image': self.press_release_photo,
                'height': self.press_release_photo_height,
                'width': self.press_release_photo_width
            }
        try:
            photo = self.photos.all()[0]
            return {
                'image': photo.thumbnail_image,
                'height': photo.thumbnail_image_height,
                'width': photo.thumbnail_image_width
            }
        except IndexError:
            return None

    @property
    def get_year(self):
        'for the slug'
        return self.start_date.year

url_tracker.track_url_changes_for_model(Exhibition)
