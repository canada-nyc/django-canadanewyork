import os

from django.db import models
from django.core.exceptions import ValidationError
from django.core.urlresolvers import reverse

import url_tracker
import dumper
import simpleimages.trackers

from apps.artists.models import Artist
from apps.photos.models import ArtworkPhoto
from libs.slugify.fields import SlugifyField
from libs.unique_boolean.fields import UniqueBooleanField
from libs.common.utils import sentance_join
from libs.ckeditor.fields import CKEditorField


class Exhibition(url_tracker.URLTrackingMixin, models.Model):
    def image_path(instance, filename):
        return os.path.join(instance.get_absolute_url()[1:], 'press_release_photos', filename)

    name = models.CharField(max_length=1000, unique_for_year='start_date')
    artists = models.ManyToManyField(Artist, related_name='exhibitions',
                                     blank=True, null=True)
    description = CKEditorField(blank=True, verbose_name='Press Release')
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    slug = SlugifyField(
        populate_from=('get_year', 'name',),
        slug_template=u'{}/{}',
        unique=True
    )

    current = UniqueBooleanField(
        help_text="Set the exhibition as the current show. Will appear on homepage",
        default=True
    )

    extra_info = models.TextField(blank=True, verbose_name='Extra Info', help_text='Only shows up on homepage, below exhibition picture and name, if it is current')

    press_release_photo = models.ImageField(
        upload_to=image_path,
        help_text='Used if it is the current exhibition, on the homepage. If not specified will use first of the uploaded photos on the homepage',
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

    class Meta:
        ordering = ["-start_date"]

    def __unicode__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('exhibition-detail', kwargs={'slug': self.slug})

    @staticmethod
    def autocomplete_search_fields():
        return ("name__icontains",)

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
                'url': self.press_release_photo.url,
                'height': self.press_release_photo_height,
                'width': self.press_release_photo_width
            }
        try:
            photo = self.photos.all()[0]
            return photo.safe_thumbnail_image
        except IndexError:
            return None

    @property
    def get_year(self):
        'for the slug'
        return self.start_date.year

    @property
    def not_group_show(self):
        if 0 < self.artists.count() < 3:
            return True

    def link_artist_if_visble(self, artist):
        if artist.visible:
            return '<a href="{}">{}</a>'.format(
                artist.get_absolute_url(),
                unicode(artist)
            )
        return unicode(artist)

    @property
    def join_artists_with_links(self):
        link_or_names = map(self.link_artist_if_visble, self.artists.all())
        return sentance_join(link_or_names)

    @property
    def join_artists(self):
        names = map(unicode, self.artists.all())
        return sentance_join(names)

    def dependent_paths(self):
        yield self.get_absolute_url()
        yield reverse('exhibition-list')
        yield reverse('exhibition-current')
        yield reverse('exhibition-press-list', kwargs={'slug': self.slug})
        for artist in self.artists.all():
            yield artist.get_absolute_url()
            yield reverse('artist-exhibition-list', kwargs={'slug': artist.slug})
        for press in self.press.all():
            yield press.get_absolute_url()


class ExhibitionPhoto(ArtworkPhoto):
    content_object = models.ForeignKey(Exhibition, related_name='photos')
    artist_text = models.CharField(
        blank=True,
        max_length=100,
        help_text='Only use if not solo artist in show',
        verbose_name='Artist'
    )

    def dependent_paths(self):
        yield self.content_object.get_absolute_url()
        if self.content_object.current:
            yield reverse('exhibition-current')

url_tracker.track_url_changes_for_model(Exhibition)
dumper.register(Exhibition)
dumper.register(ExhibitionPhoto)
simpleimages.trackers.track_model(ExhibitionPhoto)
