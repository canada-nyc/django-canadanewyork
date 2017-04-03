import copy

from django.db import models
from django.core.urlresolvers import reverse

import dumper
import simpleimages.trackers

from libs.ckeditor.fields import CKEditorField
from libs.slugify.fields import SlugifyField
from apps.photos.models import BasePhoto, image_path_function


from ..artists.models import Artist


class Book(models.Model):
    title = models.CharField(max_length=500)
    artist = models.ForeignKey(Artist, related_name='books')
    description = CKEditorField(blank=True)
    price = models.PositiveSmallIntegerField(
        blank=True,
        null=True,
        help_text="If blank, will not show buy button."
    )
    date = models.DateField(
        verbose_name='Precise Date',
        help_text='Used for ordering'
    )
    date_text = models.CharField(
        verbose_name='Inprecise Date',
        max_length=500,
        blank=True,
        help_text="If set, will display <strong>instead of</strong> the precise date."
    )

    slug = SlugifyField(
        populate_from=('artist', 'title',),
        unique=True
    )

    class Meta:
        ordering = ['artist__last_name', 'artist__first_name', '-date']
        unique_together = ['artist', 'title']

    def __str__(self):
        return "{} {}".format(self.artist, self.title)

    def clean(self):
        self.title = self.title.strip().title()

    def get_absolute_url(self):
        return reverse('book-detail', kwargs={'slug': self.slug})

    def dependent_paths(self):
        yield reverse('book-list')
        yield self.get_absolute_url()
        if self.artist:
            yield self.artist.get_absolute_url()
            yield reverse('artist-book-list', kwargs={'slug': self.artist.slug})

    def get_grid_photo(self):
        try:
            return self.photos.all()[0].safe_icon_image
        except IndexError:
            return None


def icon_image_path_function(instance, filename):
    return image_path_function('icon', instance, filename)


class BookPhoto(BasePhoto):
    content_object = models.ForeignKey(Book, related_name='photos')

    icon_image = models.ImageField(
        blank=True,
        null=True,
        editable=False,
        upload_to=icon_image_path_function,
        height_field='icon_image_height',
        width_field='icon_image_width',
        max_length=1000
    )
    icon_image_height = models.PositiveIntegerField(
        null=True,
        blank=True,
        editable=False,
    )
    icon_image_width = models.PositiveIntegerField(
        null=True,
        blank=True,
        editable=False,
    )

    transformed_fields = copy.deepcopy(BasePhoto.transformed_fields)
    transformed_fields['image']['icon_image'] = simpleimages.transforms.Scale(
        width=150,
        height=200,
    )

    @property
    def safe_icon_image(self):
        return self._get_safe_image('icon_image', 'image')


dumper.register(Book)
dumper.register(BookPhoto)
simpleimages.trackers.track_model(BookPhoto)
