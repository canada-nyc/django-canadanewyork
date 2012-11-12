from django.db import models
from django.template.defaultfilters import slugify

from apps.content_redirects.models import BaseRedirectModel


class RedirectModel(BaseRedirectModel):
    text = models.CharField(max_length=200, default='exampletext')

    def get_absolute_url(self):
        return 'text/{}'.format(slugify(self.text))


class RedirectModel_2(RedirectModel):
    def get_absolute_url(self):
        return 'text2/{}'.format(slugify(self.text))
