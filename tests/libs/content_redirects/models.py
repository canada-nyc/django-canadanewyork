from django.db import models
from django.template.defaultfilters import slugify

from libs.content_redirects.fields import RedirectField
from libs.slugify.fields import SlugifyField


class RedirectModel(models.Model):
    old_path = models.CharField(blank=True, null=True, editable=False, max_length=200)
    redirect = RedirectField()
    text = models.CharField(max_length=200, default='exampletext')

    def get_absolute_url(self):
        return 'text/{}'.format(slugify(self.text))


class RedirectSlugifyModel(models.Model):
    slug = SlugifyField(populate_from=('text',))

    old_path = models.CharField(blank=True, null=True, max_length=200, editable=False)
    redirect = RedirectField()
    text = models.CharField(max_length=200, default='exampletext')

    def get_absolute_url(self):
        return 'slug/{}'.format(self.slug)
