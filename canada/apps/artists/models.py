import os

from django.db import models
from django.db.models import permalink
from django.template.defaultfilters import slugify

from ..models import BasePhoto


class Artist(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    slug = models.SlugField(blank=True, editable=False)
    visible = models.BooleanField(
        default=False,
        help_text="Whether it appears in the Artists list")

    class Meta:
        ordering = ['last_name', 'first_name']
        unique_together = ("first_name", "last_name")

    def __unicode__(self):
        return self.slug

    def save(self, *args, **kwargs):
        self.slug = slugify('-'.join([self.first_name, self.last_name]))
        super(Artist, self).save(*args, **kwargs)

    @permalink
    def get_absolute_url(self):
        return ('artist-single', (), {
            'slug': self.slug,
            })


class ArtistPhoto(BasePhoto):
    def image_path(instance, filename):
        return os.path.join('artists', instance.artist.slug, filename)

    artist = models.ForeignKey(Artist, related_name='images')
    image = models.ImageField(upload_to=image_path)

    def __unicode__(self):
            return u'{} by {}'.format(self.title, self.artist)
