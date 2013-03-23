from django.db import models
from django.db.models import permalink
from django.db.models import Q
from django.db.models.loading import get_model
from django.contrib.contenttypes import generic

from markdown_deux.templatetags.markdown_deux_tags import markdown_allowed
import url_tracker

from libs.slugify.fields import SlugifyField
from apps.photos.models import Photo


class VisibleManager(models.Manager):
    def get_query_set(self):
        return super(VisibleManager, self).get_query_set().filter(visible=True)


class Artist(url_tracker.URLTrackingMixin, models.Model):

    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    resume = models.TextField(blank=True, null=True, help_text=markdown_allowed())
    slug = SlugifyField(populate_from=('first_name', 'last_name'))
    visible = models.BooleanField(
        default=False,
        help_text="Whether it appears in the artists list, and has an artist page")

    photos = generic.GenericRelation(Photo)

    objects = models.Manager()
    in_gallery = VisibleManager()

    class Meta:
        ordering = ['last_name', 'first_name']
        unique_together = ("first_name", "last_name")

    def __unicode__(self):
        return ' '.join([self.first_name, self.last_name])

    def clean(self):
        self.first_name = self.first_name.strip().title()
        self.last_name = self.last_name.strip().title()

        self.resume = (self.resume or '').strip()

    @permalink
    def get_absolute_url(self):
        if self.visible:
            return ('artist-detail', (), {'slug': self.slug})

    def get_press(self):
        return get_model('press', 'Press').objects.filter(
            Q(artists__in=[self]) | Q(exhibition__artists__in=[self])
        )

    @permalink
    def get_press_url(self):
        if self.visible:
            return ('artist-press-list', (), {'slug': self.slug})

    @permalink
    def get_resume_url(self):
        if self.visible:
            return ('artist-resume', (), {'slug': self.slug})

    url_tracking_methods = [
        'get_absolute_url',
        'get_press_url',
        'get_resume_url',
    ]

url_tracker.track_url_changes_for_model(Artist)
