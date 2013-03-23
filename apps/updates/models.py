from django.db import models
from django.contrib.contenttypes import generic
from django.core.urlresolvers import reverse

from markdown_deux.templatetags.markdown_deux_tags import markdown_allowed
import url_tracker

from apps.photos.models import Photo


class Update(url_tracker.URLTrackingMixin, models.Model):
    description = models.TextField(blank=True, null=True,
                                   help_text=markdown_allowed())
    post_date = models.DateTimeField(auto_now_add=True)

    photos = generic.GenericRelation(Photo)

    class Meta:
        ordering = ["-post_date"]

    def clean(self):
        self.description = self.description.strip()

    def __unicode__(self):
        return unicode('{} ({})').format(self.pk, self.post_date.year)

    def get_absolute_url(self):
        return reverse('update-single', kwargs={'pk': self.pk})

url_tracker.track_url_changes_for_model(Update)
