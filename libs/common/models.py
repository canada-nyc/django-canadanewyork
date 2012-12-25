import os

from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic

from markdown_deux.templatetags.markdown_deux_tags import markdown_allowed


class Photo(models.Model):

    def image_path(instance, filename):
        return os.path.join(
            instance.content_object.get_absolute_url()[1:],
            'photos',
            (filename or str(instance.pk)),
        )

    title = models.CharField(blank=True, max_length=400)
    caption = models.TextField(blank=True, help_text=markdown_allowed())
    image = models.ImageField(upload_to=image_path, max_length=1000)

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