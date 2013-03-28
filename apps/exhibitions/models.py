import os

from django.db import models
from django.core.exceptions import ValidationError
from django.contrib.contenttypes import generic
from django.core.urlresolvers import reverse

from markdown_deux.templatetags.markdown_deux_tags import markdown_allowed
import url_tracker

from ..artists.models import Artist
from libs.slugify.fields import SlugifyField
from apps.photos.models import Photo
from libs.unique_boolean.fields import UniqueBooleanField


class ArtistRelatedManager(models.Manager):
    def get_query_set(self):
        return super(ArtistRelatedManager, self).get_query_set().prefetch_related('artists')


class Exhibition(url_tracker.URLTrackingMixin, models.Model):

    def image_path(instance, filename):
        return os.path.join(instance.get_absolute_url()[1:], 'press_release_photos', filename)

    name = models.CharField(max_length=1000, unique_for_year='start_date')
    description = models.TextField(blank=True, help_text=markdown_allowed())
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
        help_text='Used if it is the current exhibition',
        blank=True,
        null=True
    )

    photos = generic.GenericRelation(Photo)
    objects = ArtistRelatedManager()

    class Meta:
        ordering = ["-start_date"]

    def __unicode__(self):
        if len(self.artists.all()):
            artist = self.artists.all()[0]
            return u'{}: {}'.format(artist, self.name)
        return self.name

    def get_absolute_url(self):
        return reverse('exhibition-detail', kwargs={'slug': self.slug})

    def get_press_url(self):
        '''
        So that that the exhibition-detail can link to the press detail for
        that exhibition
        '''
        return ('exhibition-press-list', (), {
            'slug': self.slug
        })

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
            return self.press_release_photo
        elif self.photos.all():
            return self.photos.all()[0].image

    def get_press_release_photo_url(self):
        '''
        For tracking of the press release photo
        '''
        if self.press_release_photo:
            return self.press_release_photo.url

    @property
    def get_year(self):
        '''
        to populate the slug
        '''
        return self.start_date.year

    url_tracking_methods = [
        'get_absolute_url',
        'get_press_release_photo_url',
        'get_press_url'
    ]

url_tracker.track_url_changes_for_model(Exhibition)
