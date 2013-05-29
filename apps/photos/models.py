import os

from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic

import simpleimages


class Photo(models.Model):

    def image_path(instance, filename):
        return os.path.join(
            'photos',
            unicode(instance.content_type),
            unicode(instance.object_id),
            filename,
        )

    def large_image_path(instance, filename):
        return os.path.join(
            'CACHE',
            'large',
            instance.image_path(filename)
        )

    def thumbnail_image_path(instance, filename):
        return os.path.join(
            'CACHE',
            'thumbnail',
            instance.image_path(filename)
        )

    title = models.CharField(blank=True, max_length=400)
    caption = models.TextField(blank=True)
    image = models.ImageField(upload_to=image_path, max_length=1000)
    thumbnail_image = models.ImageField(
        blank=True,
        null=True,
        editable=False,
        upload_to=thumbnail_image_path,
        height_field='thumbnail_image_height',
        width_field='thumbnail_image_width',
        max_length=1000
    )
    large_image = models.ImageField(
        blank=True,
        null=True,
        editable=False,
        upload_to=large_image_path,
        height_field='large_image_height',
        width_field='large_image_width',
        max_length=1000
    )
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
        blank=True
    )

    class Meta:
        ordering = ['position']

    def __unicode__(self):
            return u'{} in {} ({})'.format(
                self.title,
                self.content_object,
                self.content_type.model
            )

    def clean(self):
        self.title = self.title.strip()
        self.caption = self.caption.strip()

    transformed_fields = {
        'image': {
            'thumbnail_image': simpleimages.transforms.scale(width=600),
            'large_image': simpleimages.transforms.scale(width=800),
        }
    }


simpleimages.track_model(Photo)
