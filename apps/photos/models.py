import os
from decimal import Decimal, ROUND_DOWN
from fractions import Fraction

from django.db import models
from django.conf import settings
from django.template.loader import render_to_string

import simpleimages.transforms


def image_path_function(subfolder, instance, filename):
    return os.path.join(
        instance.content_name,
        'photos',
        subfolder,
        filename
    )


def original_image_path_function(instance, filename):
    return image_path_function('original', instance, filename)


def thumbnail_image_path_function(instance, filename):
    return image_path_function('thumbnail', instance, filename)


def large_image_path_function(instance, filename):
    return image_path_function('large', instance, filename)


class BasePhoto(models.Model):
    title = models.CharField(blank=True, max_length=400)
    caption = models.TextField(blank=True, verbose_name='Extra Text')

    image = models.ImageField(
        upload_to=original_image_path_function,
        max_length=1000,
        verbose_name='Image File'
    )
    thumbnail_image = models.ImageField(
        blank=True,
        null=True,
        editable=False,
        upload_to=thumbnail_image_path_function,
        height_field='thumbnail_image_height',
        width_field='thumbnail_image_width',
        max_length=1000
    )
    large_image = models.ImageField(
        blank=True,
        null=True,
        editable=False,
        upload_to=large_image_path_function,
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
        default=0,
        null=False,
        blank=False
    )

    class Meta:
        ordering = ['position']
        abstract = True

    def __str__(self):
        return '#{} {}'.format(self.position + 1, self.title)

    transformed_fields = {
        'image': {
            'thumbnail_image': simpleimages.transforms.Scale(height=500),
            'large_image': simpleimages.transforms.Scale(height=800),
        }
    }

    def dependent_paths(self):
        yield self.content_object.get_absolute_url()

    caption_template = 'photos/full_caption.html'

    @property
    def content_name(self):
        return os.path.join(
            self.content_object._meta.app_label,
            str(self.content_object.pk),
        )

    @property
    def full_caption(self):
        return render_to_string(self.caption_template, {'photo': self})

    def _get_safe_image(self, image_field_name, backup_image_field_name):
        '''
        Returns a dictionary with the URL, width, and height of the image
        in ``image_field_name``.

        It gets the dimensions from the cached dimensions fields. Django
        provides a way to cache image dimensions in other fields,
        so that it won't have to retrieve the image every time you want
        its dimensions. It assumes these fields are named the same
        as the original image field with a `_width` or `_height` suffix.

        So if ``image_field_name`` was ``thumbnail``, it would return
        dimensions from the fields ``thumbnail_width`` and ``thumbnail_height``.

        If the image in ``image_field_name`` is blank, it will return the
        ``backup_image_field_name`` image instead.
        '''

        image_field = getattr(self, image_field_name)
        if not image_field:
            return getattr(self, backup_image_field_name)

        if settings.CANADA_IMAGE_DIMENSION_FIELDS:
            width, height = [getattr(self, image_field_name + suffix) for suffix in ['_width', '_height']]
        else:
            width, height = image_field.width, image_field.height
        return {
            'url': image_field.url,
            'width': width,
            'height': height,
        }

    @property
    def safe_thumbnail_image(self):
        return self._get_safe_image('thumbnail_image', 'image')

    @property
    def safe_large_image(self):
        return self._get_safe_image('large_image', 'image')


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

    def remove_exponent(self, d):
        '''
        Remove exponent and trailing zeros.

        >>> remove_exponent(Decimal('5E+3'))
        Decimal('5000')
        '''
        return d.quantize(Decimal(1)) if d == d.to_integral() else d.normalize()

    def round_decimal(self, number):
        return self.remove_exponent(Decimal(number).normalize())

    @property
    def dimensions(self):
        return list(map(self.round_decimal, [_f for _f in [self.height, self.width, self.depth] if _f]))

    def convert_inches_to_cm(self, inches):
        cm = inches * Decimal(self.INCHES_PER_CM)
        return cm.quantize(self.DECIMAL_PLACES)

    @property
    def dimensions_cm(self):
        return list(map(self.round_decimal, list(map(self.convert_inches_to_cm, self.dimensions))))

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
            inches_dimensions = list(map(self.decimal_to_fraction, self.dimensions))
            cm_dimensions = list(map(str, self.dimensions_cm))
            return '{} in ({} cm)'.format(' x '.join(inches_dimensions), ' x '.join(cm_dimensions))
