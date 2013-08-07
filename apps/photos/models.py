import os
from decimal import Decimal

from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic
from django.template.loader import render_to_string
from django.db import models

import simpleimages
import dumper


INCHES_PER_CM = 2.54

dimension_field_attributes = {
    'blank': True,
    'null': True,
    'max_digits': 6,
    'decimal_places': 2,
}

DECIMAL_PLACES = Decimal(10) ** (-1 * dimension_field_attributes['decimal_places'])

class Photo(models.Model):
    def image_path_function(subfolder):
        return lambda instance, filename: os.path.join(
            'photos',
            subfolder,
            unicode(instance.content_type),
            unicode(instance.object_id),
            filename
        )
    title = models.CharField(blank=True, max_length=400)

    caption = models.TextField(blank=True, verbose_name='Extra Text')

    year = models.PositiveIntegerField(null=True, blank=True)
    medium = models.CharField(blank=True, max_length=100)
    height = models.DecimalField(verbose_name='Height (in)', **dimension_field_attributes)
    width = models.DecimalField(verbose_name='Width (in)', **dimension_field_attributes)
    depth = models.DecimalField(verbose_name='Depth (in)', **dimension_field_attributes)

    image = models.ImageField(
        upload_to=image_path_function('original'),
        max_length=1000,
        help_text="To change image files on this photo, delete it and create a new one for the image",
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

    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    content_object = generic.GenericForeignKey()

    position = models.PositiveSmallIntegerField(
        "Position",
        null=True,
        blank=True,
    )

    class Meta:
        ordering = ['position']

    def __unicode__(self):
        if self.position:
            return u'#{} {}'.format(self.position + 1, self.title)
        return self.title

    def clean(self):
        self.title = self.title.strip()
        self.caption = self.caption.strip()

    transformed_fields = {
        'image': {
            'thumbnail_image': simpleimages.transforms.scale(height=600),
            'large_image': simpleimages.transforms.scale(height=800),
        }
    }

    def dependent_paths(self):
        yield self.content_object.get_absolute_url()

    @property
    def dimensions(self):
        return filter(None, [self.height, self.width, self.depth])

    def convert_inches_to_cm(self, inches):
        cm = inches * Decimal(INCHES_PER_CM)
        return cm.quantize(DECIMAL_PLACES)

    @property
    def dimensions_cm(self):
        return map(self.convert_inches_to_cm, self.dimensions)

    @property
    def full_caption(self):
        return render_to_string('photos/full_caption.html', {'photo': self})

    @classmethod
    def create_mock(self):
        mock_photo = self(
            title='<title>',
            year='<year>',
            medium='<medium>',
            height='<height>',
            width='<width>',
            depth='<depth>',
            caption='<extra text>'
        )
        def convert_mock_dimension_field_name_to_cm(field_name):
            '''
            <width> -> <width_cm>
            '''
            return field_name[:-1] + '_cm>'
        mock_photo.convert_inches_to_cm = convert_mock_dimension_field_name_to_cm
        return mock_photo

simpleimages.track_model(Photo)
dumper.register(Photo)
