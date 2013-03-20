import os

from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic

import url_tracker
import simpleimages


class Photo(models.Model):

    def image_path(instance, filename):
        return os.path.join(
            'photos',
            instance.content_object.get_absolute_url()[1:],
            (filename or str(instance.pk)),
        )

    def image_path_large(instance, filename):
        return os.path.join(
            'photos',
            'transformed',
            'large',
            instance.content_object.get_absolute_url()[1:],
            (filename or str(instance.pk)),
        )

    def image_path_thumb(instance, filename):
        return os.path.join(
            'photos',
            'transformed',
            'thumb',
            instance.content_object.get_absolute_url()[1:],
            (filename or str(instance.pk)),
        )

    title = models.CharField(blank=True, max_length=400)
    caption = models.TextField(blank=True)
    image = models.ImageField(upload_to=image_path, max_length=1000)
    image_large = models.ImageField(
        upload_to=image_path_large,
        max_length=1000,
        blank=True,
        null=True,
        editable=False
    )
    image_thumb = models.ImageField(
        upload_to=image_path_thumb,
        max_length=1000,
        blank=True,
        null=True,
        editable=False
    )

    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    content_object = generic.GenericForeignKey('content_type', 'object_id')

    position = models.PositiveSmallIntegerField("Position", null=True, blank=True)

    class Meta:
        ordering = ['position']

    def __unicode__(self):
            return u'{} in {} ({})'.format(self.title,
                                           self.content_object,
                                           self.content_type.model)

    def clean(self):
        self.title = self.title.strip()
        self.caption = self.caption.strip()

    transformed_fields = {
        'image': {
            'image_large': simpleimages.transforms.scale(width=800),
            'image_thumb': simpleimages.transforms.scale(width=100)
        }
    }

    def get_image_url(self):
        if self.image:
            return self.image.url

url_tracker.track_url_changes_for_model(Photo, 'get_image_url')
simpleimages.track_model(Photo)
