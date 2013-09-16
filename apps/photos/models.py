import os
from decimal import Decimal, ROUND_DOWN
from fractions import Fraction

from django.db import models
from django.template.loader import render_to_string

import simpleimages.transforms


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
        if self.position is not None:
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
        'max_digits': 10,
        'decimal_places': 4,
    }

    DECIMAL_PLACES = Decimal(10) ** (-1 * dimension_field_attributes['decimal_places'])

    date = models.CharField(blank=True, max_length=100)
    medium = models.CharField(blank=True, max_length=100)

    height = models.DecimalField(verbose_name='Height (in)', **dimension_field_attributes)
    width = models.DecimalField(verbose_name='Width (in)', **dimension_field_attributes)
    depth = models.DecimalField(verbose_name='Depth (in)', **dimension_field_attributes)

    dimensions_text = models.CharField(
        verbose_name='Dimensions',
        blank=True,
        max_length=300,
        help_text="Only use if the seperate dimension fields do not apply to this piece."
    )

    class Meta:
        ordering = ['position']
        abstract = True

    caption_template = 'photos/full_caption.html'

    def remove_exponent(self, d):
        '''Remove exponent and trailing zeros.

        >>> remove_exponent(Decimal('5E+3'))
        Decimal('5000')

        '''
        return d.quantize(Decimal(1)) if d == d.to_integral() else d.normalize()

    def round_decimal(self, number):
        return self.remove_exponent(Decimal(number).normalize())

    @property
    def dimensions(self):
        return map(self.round_decimal, filter(None, [self.height, self.width, self.depth]))

    def convert_inches_to_cm(self, inches):
        cm = inches * Decimal(self.INCHES_PER_CM)
        return cm.quantize(self.DECIMAL_PLACES)

    @property
    def dimensions_cm(self):
        return map(self.round_decimal, map(self.convert_inches_to_cm, self.dimensions))

    def decimal_to_fraction(self, decimal):
        integer = decimal.to_integral_value(ROUND_DOWN)
        decimal_part = decimal - integer
        if not decimal_part:
            return str(integer)
        fraction = Fraction(decimal_part)
        fraction_string = '{}/{}'.format(fraction.numerator, fraction.denominator)
        if integer:
            return '{} {}'.format(integer, fraction_string)
        return fraction_string

    @property
    def full_dimensions(self):
        if self.dimensions_text:
            return self.dimensions_text
        if self.dimensions:
            inches_dimensions = map(self.decimal_to_fraction, self.dimensions)
            cm_dimensions = map(str, self.dimensions_cm)
            return '{} in ({} cm)'.format(' x '.join(inches_dimensions), ' x '.join(cm_dimensions))
