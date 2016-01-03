from django.db import models
from django_fake_model import models as f

from libs.slugify.fields import SlugifyField


class RelatedModel(f.FakeModel):
    text = models.CharField(max_length=400)


class SlugifyModel(f.FakeModel):
    text = models.CharField(max_length=400)
    related_model = models.ForeignKey(RelatedModel)
    slug = SlugifyField(populate_from=('text', 'related_model'))


class SlugifyUniqueModel(f.FakeModel):
    text = models.CharField(max_length=400)
    slug = SlugifyField(populate_from=('text',), unique=True)


class SlugifyTemplateModel(f.FakeModel):
    text = models.CharField(max_length=400)
    text2 = models.CharField(max_length=400)
    slug = SlugifyField(
        populate_from=('text', 'text2'),
        slug_template='{}/{}'
    )
