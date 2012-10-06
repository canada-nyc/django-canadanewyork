from django.db import models

from markdown_deux.templatetags.markdown_deux_tags import markdown_allowed


class BasePhoto(models.Model):
    title = models.CharField(blank=True, max_length=20)
    caption = models.CharField(blank=True, max_length=100,
                               help_text=markdown_allowed())

    position = models.PositiveSmallIntegerField("Position")

    class Meta:
        abstract = True
        ordering = ['position']
