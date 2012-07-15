import os

from django.db import models
from django.db.models import permalink
from django.template.defaultfilters import slugify
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
        return '{}({})'.format(self.name, self.start_date.strftime("%Y"))

    def save(self):
        self.slug = slugify('-'.join([self.start_date.strftime("%Y"),
                                      self.name]))
        super(Exhibition, self).save()

    @permalink
    def get_absolute_url(self):
        return ('canada.exhibitions.views.single', (), {
            'year': self.start_date.strftime("%Y"),
            'slug': self.slug
        })

    def clean(self):
        if not self.start_date <= self.end_date:
            raise ValidationError('Start date can not be after end date')

    def get_first_image_or_none(self):
        if self.images.all().count() > 0:
            return self.images.all()[0]


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
