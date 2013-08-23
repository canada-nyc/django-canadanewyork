from django.db import models
from django.core.urlresolvers import reverse

import url_tracker
import dumper

from apps.photos.models import BasePhoto


class Update(url_tracker.URLTrackingMixin, models.Model):
    description = models.TextField(blank=True)
    post_date = models.DateField(auto_now_add=True)

    class Meta:
        ordering = ["-post_date"]

    def clean(self):
        self.description = self.description.strip()

    def __unicode__(self):
        return unicode(self.post_date.isoformat())

    def get_absolute_url(self):
        return reverse('update-detail', kwargs={'pk': self.pk})

    def dependent_paths(self):
        yield self.get_absolute_url()


class UpdatePhoto(BasePhoto):
    content_object = models.ForeignKey(Update, related_name='photos')

url_tracker.track_url_changes_for_model(Update)
dumper.register(Update)
dumper.register(UpdatePhoto)
