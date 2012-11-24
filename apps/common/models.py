import os

from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic


class Photo(models.Model):

    def image_path(instance, filename):
        return os.path.join(instance.content_type.model,
                            instance.content_object.slug,
                            filename)

    title = models.CharField(blank=True, max_length=20)
    caption = models.CharField(blank=True, max_length=100)
    image = models.ImageField(upload_to=image_path)

    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    content_object = generic.GenericForeignKey('content_type', 'object_id')

    position = models.PositiveSmallIntegerField("Position")

    class Meta:
        ordering = ['position']

    def __unicode__(self):
            return u'{} in {} ({})'.format(self.title,
                                           self.content_object,
                                           self.content_type.model)
