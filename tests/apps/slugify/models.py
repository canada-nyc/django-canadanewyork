from django.db import models

from apps.slugify.fields import SlugifyField


class RelatedModel(models.Model):
    text = models.CharField(max_length=200)


class SlugifyModel(models.Model):
    text = models.CharField(max_length=200)
    text2 = models.CharField(max_length=200)
    related_model = models.ForeignKey(RelatedModel)
    slug = SlugifyField(populate_from=('text', 'related_model'))
