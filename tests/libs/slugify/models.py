from django.db import models

from libs.slugify.fields import SlugifyField


class RelatedModel(models.Model):
    text = models.CharField(max_length=400)


class SlugifyModel(models.Model):
    text = models.CharField(max_length=400)
    related_model = models.ForeignKey(RelatedModel)
    slug = SlugifyField(populate_from=('text', 'related_model'))


class SlugifyDateModel(models.Model):
    text = models.CharField(max_length=400)
    date = models.DateTimeField(auto_now=True)
    slug = SlugifyField(populate_from=('text', lambda m: m.date.year))
