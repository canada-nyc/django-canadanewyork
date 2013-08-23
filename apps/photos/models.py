import os
from decimal import Decimal

from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic
from django.template.loader import render_to_string

import simpleimages.transforms
import simpleimages.trackers
import dumper


class BasePhoto(models.Model):
    def image_path_function(subfolder):
        return lambda instance, filename: os.path.join(
            instance.content_name,
            'photos',
            subfolder,
            filename
        )

    title = models.CharField(blank=True, max_length=400)
    caption = models.TextField(blank=True, verbose_name='Extra Text')

    image = models.ImageField(
        upload_to=image_path_function('original'),
        max_length=1000,
        verbose_name='Image File'
    )
    thumbnail_image = models.ImageField(
        blank=True,
        null=True,
        editable=False,
        upload_to=image_path_function('thumbnail'),
        height_field='thumbnail_image_height',
        width_field='thumbnail_image_width',
        max_length=1000
    )
    large_image = models.ImageField(
        blank=True,
        null=True,
        editable=False,
        upload_to=image_path_function('large'),
        height_field='large_image_height',
        width_field='large_image_width',
        max_length=1000
    )
    # cached dimension fields
    thumbnail_image_height = models.PositiveIntegerField(
        null=True,
        blank=True,
        editable=False,
    )
    thumbnail_image_width = models.PositiveIntegerField(
        null=True,
        blank=True,
        editable=False,
    )
    large_image_height = models.PositiveIntegerField(
        null=True,
        blank=True,
        editable=False,
    )
    large_image_width = models.PositiveIntegerField(
        null=True,
        blank=True,
        editable=False,
    )

    position = models.PositiveSmallIntegerField(
        verbose_name='',
        null=True,
        blank=True,
    )

    class Meta:
        ordering = ['position']
        abstract = True

    def __unicode__(self):
        if self.position:
            return u'#{} {}'.format(self.position + 1, self.title)
        return self.title

    transformed_fields = {
        'image': {
            'thumbnail_image': simpleimages.transforms.Scale(height=600),
            'large_image': simpleimages.transforms.Scale(height=800),
        }
    }

    def dependent_paths(self):
        yield self.content_object.get_absolute_url()

    @property
    def content_name(self):
        return os.path.join(
            unicode(self.content_object._meta.app_label),
            unicode(self.content_object.pk),
        )

    @property
    def full_caption(self):
        return render_to_string(self.caption_template, {'photo': self})

    @property
    def safe_thumbnail_image(self):
        if self.thumbnail_image:
            return {
                'url': self.thumbnail_image.url,
                'width': self.thumbnail_image_width,
                'height': self.thumbnail_image_height
            }
        return self.image

    @property
    def safe_large_image(self):
        if self.large_image:
            return {
                'url': self.large_image.url,
                'width': self.large_image_width,
                'height': self.large_image_height
            }
        return self.image


class ArtworkPhoto(BasePhoto):
    INCHES_PER_CM = 2.54

    dimension_field_attributes = {
        'blank': True,
        'null': True,
        'max_digits': 6,
        'decimal_places': 2,
    }

    DECIMAL_PLACES = Decimal(10) ** (-1 * dimension_field_attributes['decimal_places'])

    year = models.PositiveIntegerField(null=True, blank=True)
    medium = models.CharField(blank=True, max_length=100)

    height = models.DecimalField(verbose_name='Height (in)', **dimension_field_attributes)
    width = models.DecimalField(verbose_name='Width (in)', **dimension_field_attributes)
    depth = models.DecimalField(verbose_name='Depth (in)', **dimension_field_attributes)

    class Meta:
        abstract = True

    caption_template = 'photos/full_caption.html'

    def round_decimal(self, number):
        return Decimal(number).normalize()

    @property
    def dimensions(self):
        return map(self.round_decimal, filter(None, [self.height, self.width, self.depth]))

    def convert_inches_to_cm(self, inches):
        cm = inches * Decimal(self.INCHES_PER_CM)
        return cm.quantize(self.DECIMAL_PLACES)

    @property
    def dimensions_cm(self):
        return map(self.round_decimal, map(self.convert_inches_to_cm, self.dimensions))


class Photo(ArtworkPhoto):
    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    content_object = generic.GenericForeignKey()

    artist_text = models.CharField(blank=True, max_length=100, help_text='only specify in group show', verbose_name='Artist')

    @property
    def content_name(self):
        return os.path.join(
            unicode(self.content_type),
            unicode(self.object_id),
        )

simpleimages.trackers.track_model(Photo)
dumper.register(Photo)
