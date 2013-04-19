import os

from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic

from simpleimages.transforms import scale
from simpleimages.trackers import track_model
import url_tracker


class Photo(url_tracker.URLTrackingMixin, models.Model):

    def image_path(instance, filename):
        return os.path.join(
            'photos',
            instance.content_object.get_absolute_url()[1:],
            (filename or str(instance.pk)),
        )

    def image_path_gallery(instance, filename):
        return os.path.join(
            'photos_resized',
            'gallery',
            instance.content_object.get_absolute_url()[1:],
            (filename or str(instance.pk)),
        )

    def image_path_thumb(instance, filename):
        return os.path.join(
            'photos_resized',
            'gallery',
            instance.content_object.get_absolute_url()[1:],
            (filename or str(instance.pk)),
        )

    title = models.CharField(blank=True, max_length=400)
    caption = models.TextField(blank=True)
    image = models.ImageField(upload_to=image_path, max_length=1000)
    image_gallery = models.ImageField(upload_to=image_path_gallery, max_length=1000)
    image_thumb = models.ImageField(upload_to=image_path_thumb, max_length=1000)

    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    content_object = generic.GenericForeignKey('content_type', 'object_id')

    position = models.PositiveSmallIntegerField("Position", null=True, blank=True)

    transformed_fields = {
        'image': {
            'image_gallery': scale(width=800),
            'image_thumb': scale(width=600),
        }
    }

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

track_model(Photo)
