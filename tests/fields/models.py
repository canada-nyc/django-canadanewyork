from django.db import models

from canada.apps.fields import UniqueBooleanField


class UniqueBooleanModel(models.Model):
    unique_boolean = UniqueBooleanField()

    def __unicode__(self):
        return str(self.unique_boolean)
