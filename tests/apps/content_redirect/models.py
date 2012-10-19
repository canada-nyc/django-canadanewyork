from django.db import models
from django.db.models import permalink
from django.template.defaultfilters import slugify
from django.contrib.redirects.models import Redirect

from apps.model_redirects.fields import RedirectOldPathField


class RedirectModel(models.Model):
    text = models.CharField(max_length=200, blank=True, null=True)
    redirect = models.OneToOneField(Redirect)
    old_path = RedirectOldPathField('redirect')

    @permalink
    def get_absolute_url(self):
        return 'text/{}'.format(slugify(self.text))


class RedirectModel_2(models.Model):
    text = models.CharField(max_length=200, blank=True, null=True)
    redirect = models.OneToOneField(Redirect)
    old_path = RedirectOldPathField('redirect')

    @permalink
    def get_absolute_url(self):
        return 'text2/{}'.format(slugify(self.text))
