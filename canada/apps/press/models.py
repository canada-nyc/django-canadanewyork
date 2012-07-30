import os

from django.db.models import permalink
from django.template.defaultfilters import slugify
from django.db import models

from ..artists.models import Artist
from ..exhibitions.models import Exhibition


class Publisher(models.Model):
    name = models.CharField(max_length=50)
    homepage = models.URLField(null=True, blank=True)
    slug = models.SlugField(editable=False, unique=True)

    class Meta:
        ordering = ['name']

    def __unicode__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Publisher, self).save(*args, **kwargs)

    @permalink
    def get_absolute_url(self):
        return ('publisher-detail', (), {
            'slug': self.slug,
            })


class Press(models.Model):
    def image_path(instance, filename):
        return os.path.join('press',
                            str(instance.press.date.year),
                            instance.exhibition.slug,
                            filename)

    title = models.CharField(max_length=50)
    image = models.ImageField(null=True, blank=True, upload_to=image_path)
    url = models.URLField(null=True, blank=True)
    date = models.DateField()

    publisher = models.ForeignKey(Publisher, related_name='articles')
    author = models.CharField(max_length=60, blank=True)
    artists = models.ManyToManyField(Artist, blank=True, null=True,
                                     related_name='press')
    exhibition = models.ForeignKey(Exhibition, blank=True, null=True,
                                   related_name='press')

    slug = models.SlugField(editable=False, unique_for_year='date')

    class Meta:
        ordering = ['-date']
        verbose_name_plural = "press"

    def __unicode__(self):
        return u'{} ({})'.format(self.title, self.date.year)

    def save(self):
        self.slug = slugify(self.title)
        super(Press, self).save()

    @permalink
    def get_absolute_url(self):
        return ('press-detail', (), {
            'slug': self.slug,
            'year': self.date.year
            })
