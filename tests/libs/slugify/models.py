from django.db import models

from libs.slugify.fields import SlugifyField


class RelatedModel(models.Model):
    text = models.CharField(max_length=400)


class SlugifyModel(models.Model):
    text = models.CharField(max_length=400)
    related_model = models.ForeignKey(RelatedModel)
    slug = SlugifyField(populate_from=('text', 'related_model'))


class SlugifyUniqueModel(models.Model):
    text = models.CharField(max_length=400)
    slug = SlugifyField(populate_from=('text',), unique=True)


class SlugifyTemplateModel(models.Model):
    text = models.CharField(max_length=400)
    text2 = models.CharField(max_length=400)
    slug = SlugifyField(
        populate_from=('text', 'text2'),
        slug_template='{}/{}'
    )
