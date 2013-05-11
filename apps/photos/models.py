import os

from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic

import url_tracker


class Photo(url_tracker.URLTrackingMixin, models.Model):

    def image_path(instance, filename):
        return os.path.join(
            'photos',
            unicode(instance.content_type),
            unicode(instance.object_id),
            filename,
        )

    title = models.CharField(blank=True, max_length=400)
    caption = models.TextField(blank=True)
    image = models.ImageField(upload_to=image_path, max_length=1000)

    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    content_object = generic.GenericForeignKey('content_type', 'object_id')

    position = models.PositiveSmallIntegerField("Position", null=True, blank=True)

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
