import os

from django.db import models
from django.db.models import permalink
from django.core.exceptions import ValidationError
from django.db.models.loading import get_model

from markdown_deux.templatetags.markdown_deux_tags import markdown_allowed

from ..artists.models import Artist
from ..common.models import BasePhoto
from ..slugify.fields import SlugifyField


class Exhibition(models.Model):
    name = models.CharField(max_length=30, unique_for_year='start_date')
    description = models.TextField(blank=True, help_text=markdown_allowed())
    artists = models.ManyToManyField(Artist, related_name='exhibitions')
    start_date = models.DateField()
    end_date = models.DateField()
    slug = SlugifyField(populate_from=('name',))

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

    def clean(self):
        if not self.start_date <= self.end_date:
            raise ValidationError('Start date can not be after end date')

    def get_press(self):
        return get_model('press', 'Press').objects.filter(exhibition=self)

    @permalink
    def get_press_url(self):
        return ('exhibition-press-list', (), {
            'year': self.start_date.year,
            'slug': self.slug
        })


class ExhibitionPhoto(BasePhoto):
    def image_path(instance, filename):
        return os.path.join(
            'exhibitions',
            str(instance.exhibition.slug),
            (str(instance.position) + filename))

    exhibition = models.ForeignKey(Exhibition, related_name='images')
    image = models.ImageField(upload_to=image_path)

    def __unicode__(self):
        return 'in {}, position is {}'.format(self.exhibition, self.position)
