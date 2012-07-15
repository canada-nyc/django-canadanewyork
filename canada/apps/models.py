from django.db import models


class BasePhoto(models.Model):
    title = models.CharField(blank=True, max_length=50)
    medium = models.CharField(blank=True, max_length=50)
    year = models.PositiveIntegerField(null=True, blank=True)
    dimensions = models.CharField(blank=True, max_length=30, )

    position = models.PositiveSmallIntegerField()

    class Meta:
        abstract = True
        ordering = ['position']
