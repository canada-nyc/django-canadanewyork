from django.db import models

from apps.base.fields import UniqueBooleanField


class UniqueBooleanModel(models.Model):
    unique_boolean = UniqueBooleanField()

    def __unicode__(self):
        return str(self.unique_boolean)
