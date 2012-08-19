import os

from django.db import models
from django.db.models import permalink
from django.template.defaultfilters import slugify, date
from django.core.exceptions import ValidationError

from ..artists.models import Artist
from ..models import BasePhoto


class Exhibition(models.Model):
    name = models.CharField(max_length=30, unique_for_year='start_date')
    description = models.TextField(blank=True)
    artists = models.ManyToManyField(Artist, related_name='exhibitions')
    start_date = models.DateField()
    end_date = models.DateField()
    slug = models.SlugField(blank=True, editable=False)

    class Meta:
        ordering = ["-start_date"]

    def __unicode__(self):
        return '{}({})'.format(self.name, self.start_date.year)

    def save(self):
        self.slug = slugify(self.name)
        super(Exhibition, self).save()

    @permalink
    def get_absolute_url(self):
        return ('exhibition-detail', (), {
            'year': self.start_date.year,
            'slug': self.slug,
            'press': ''
        })

    def clean(self):
        if not self.start_date <= self.end_date:
            raise ValidationError('Start date can not be after end date')

    def get_first_image_or_none(self):
        if self.images.all().count() > 0:
            return self.images.all()[0]

    def full_date(self):
        begin_time = 'F j'
        if self.start_date.year != self.end_date.year:
            end_time = 'F j, Y'
            begin_time = 'F j, Y'
        elif self.start_date.month != self.start_date.month:
            end_time = 'F j, Y'
        elif self.start_date.day != self.start_date.day:
            end_time = 'j, Y'
        else:
            return date(self.start_date, 'F j, Y')
        return ' - '.join([date(self.start_date, begin_time), date(self.start_date, end_time)])


class ExhibitionPhoto(BasePhoto):
    def image_path(instance, filename):
        return os.path.join(
            'exhibitions',
            str(instance.exhibition.slug),
            (str(instance.position) + filename)
           )

    exhibition = models.ForeignKey(Exhibition, related_name='images')
    image = models.ImageField(upload_to=image_path)

    def __unicode__(self):
        return 'in {}, position is {}'.format(self.exhibition, self.position)
