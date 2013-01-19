import os

from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic

from libs.update_related.models import RedirectField


class Photo(models.Model):

    def image_path(instance, filename):
        return os.path.join(
            instance.content_object.get_absolute_url()[1:],
            'photos',
            (filename or str(instance.pk)),
        )

    title = models.CharField(blank=True, max_length=400)
    caption = models.TextField(blank=True)
    image = models.ImageField(upload_to=image_path, max_length=1000)

    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    content_object = generic.GenericForeignKey('content_type', 'object_id')

    position = models.PositiveSmallIntegerField("Position", null=True, blank=True)

    old_image_path = models.CharField(blank=True, max_length=1000)
    image_redirect = RedirectField(model_to_related={
        'old_path': lambda model: model.old_image_path,
        'new_path': lambda model: model.image.url,
    })

    class Meta:
        ordering = ['position']

    def __unicode__(self):
            return u'{} in {} ({})'.format(self.title,
                                           self.content_object,
                                           self.content_type.model)

    def clean(self):
        self.title = self.title.strip()
        self.caption = self.caption.strip()
