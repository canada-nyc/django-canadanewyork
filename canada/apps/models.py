from django.db import models


class BasePhoto(models.Model):
    title = models.CharField(blank=True, max_length=20)
    caption = models.CharField(blank=True, max_length=100)

    position = models.PositiveSmallIntegerField()

    class Meta:
        abstract = True
        ordering = ['position']
