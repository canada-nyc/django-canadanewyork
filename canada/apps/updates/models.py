import os

from django.db import models
from django.db.models import permalink
from django.template.defaultfilters import slugify

from ..artists.models import Artist
from ..exhibitions.models import Exhibition
from ..models import BasePhoto


class Update(models.Model):

    name = models.CharField(max_length=30, unique_for_year='post_date')
    description = models.TextField(blank=True, null=True)
    artists = models.ManyToManyField(Artist, blank=True, null=True)
    exhibition = models.ForeignKey(Exhibition, blank=True, null=True)
    post_date = models.DateTimeField(auto_now_add=True)
    slug = models.SlugField(blank=True, editable=False)

    class Meta:
        ordering = ["-post_date"]

    def __unicode__(self):
        return '{} ({})'.format(self.name, self.post_date.year)

    def save(self, *args, **kwargs):
        import datetime
        year = str(datetime.datetime.now().year)
        if self.post_date:
            year = self.post_date.year
        self.slug = slugify('-'.join([year, self.name]))
        super(Update, self).save(*args, **kwargs)

    @permalink
    def get_absolute_url(self):
        return ('update-single', (), {
            'slug': self.slug,
            })

    def get_first_image_or_none(self):
        if self.images.all().count() > 0:
            return self.images.all()[0]


class UpdatePhoto(BasePhoto):
    def image_path(instance, filename):
        return os.path.join('updates',
                            str(instance.update.post_date.year),
                            str(instance.update.slug),
                            filename)

    update = models.ForeignKey(Update, related_name='images')
    image = models.ImageField(upload_to=image_path)

    def __unicode__(self):
        return 'in {}, position is {}'.format(self.update, self.position)
