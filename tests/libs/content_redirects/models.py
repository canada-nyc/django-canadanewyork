from django.db import models
from django.template.defaultfilters import slugify

from libs.content_redirects.models import BaseRedirectModel
from libs.slugify.fields import SlugifyField


class RedirectModel(BaseRedirectModel):
    text = models.CharField(max_length=200, default='exampletext')

    def get_absolute_url(self):
        return 'text/{}'.format(slugify(self.text))


class RedirectSlugifyModel(RedirectModel):
    slug = SlugifyField(populate_from=('text',))

    def get_absolute_url(self):
        return 'slug/{}'.format(self.slug)
