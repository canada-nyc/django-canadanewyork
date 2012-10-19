from django.db import models
from django.db.models import permalink
from django.template.defaultfilters import slugify

from apps.model_redirects.fields import RedirectOldPathField


class ContentRedirectModel(models.Model):
    text = models.CharField(max_length=200, blank=True, null=True)
    old_path = RedirectOldPathField()

    @permalink
    def get_absolute_url(self):
        return 'text/{}'.format(slugify(self.some_text))


class ContentRedirectModel_2(models.Model):
    text = models.CharField(max_length=200, blank=True, null=True)
    old_path = RedirectOldPathField()

    @permalink
    def get_absolute_url(self):
        return 'text2/{}'.format(slugify(self.some_text))
