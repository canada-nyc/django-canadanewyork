from django.db import models
from django.db.models import permalink
from django.core.exceptions import ValidationError
from django.db.models.loading import get_model
from django.contrib.contenttypes import generic

from markdown_deux.templatetags.markdown_deux_tags import markdown_allowed

from ..artists.models import Artist
from libs.slugify.fields import SlugifyField
from libs.content_redirects.fields import RedirectField
from libs.common.models import Photo


class Exhibition(models.Model):
    name = models.CharField(max_length=1000, unique_for_year='start_date')
    description = models.TextField(blank=True, help_text=markdown_allowed())
    artists = models.ManyToManyField(Artist, related_name='exhibitions',
                                     blank=True, null=True)
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    slug = SlugifyField(populate_from=('name',))

    old_path = models.CharField(blank=True, null=True, editable=False, max_length=2000)
    redirect = RedirectField()

    photos = generic.GenericRelation(Photo)

    class Meta:
        ordering = ["-start_date"]

    def __unicode__(self):
        return '{}({})'.format(self.name, self.start_date.year)

    @permalink
    def get_absolute_url(self):
        return ('exhibition-detail', (), {
            'year': self.start_date.year,
            'slug': self.slug,
        })

    def save(self, *args, **kwargs):
        if self.start_date == self.end_date:
            self.end_date = None
        super(Exhibition, self).save(*args, **kwargs)
        return self

    def clean(self):
        if self.end_date and self.start_date > self.end_date:
            raise ValidationError('Start date can not be after end date')
        self.name = self.name.strip()
        self.description = self.description.strip()

        self.name = self.name.strip()
        self.description = self.description.strip()

    def get_press(self):
        return get_model('press', 'Press').objects.filter(exhibition=self)

    @permalink
    def get_press_url(self):
        return ('exhibition-press-list', (), {
            'year': self.start_date.year,
            'slug': self.slug
        })
