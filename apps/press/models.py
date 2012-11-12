import os

from django.db.models import permalink
from django.db import models
from django.core.exceptions import ValidationError

from ..artists.models import Artist
from ..exhibitions.models import Exhibition
from ..slugify.fields import SlugifyField
from ..content_redirects.models import BaseRedirectModel


class Press(BaseRedirectModel):
    def image_path(instance, filename):
        return os.path.join('press',
                            str(instance.date.year),
                            instance.exhibition.slug,
                            filename)

    title = models.CharField(max_length=50)
    image = models.ImageField(null=True, blank=True, upload_to=image_path)
    link = models.URLField(null=True, blank=True, verbose_name=u'External link')
    date = models.DateField()

    publisher = models.CharField(max_length=50)
    author = models.CharField(max_length=60, blank=True, null=True)
    artists = models.ManyToManyField(Artist, blank=True, null=True,
                                     related_name='press',)
    exhibition = models.ForeignKey(Exhibition, blank=True, null=True,
                                   related_name='press',)
    slug = SlugifyField(populate_from=('title',))

    class Meta:
        ordering = ['-date']
        verbose_name_plural = "press"

    def __unicode__(self):
        return u'{} ({})'.format(self.title, self.date.year)

    def clean(self):
        if not self.image and not self.link:
            raise ValidationError('Either upload an image or add a link.')

    @permalink
    def get_absolute_url(self):
        return ('press-detail', (), {
            'slug': self.slug,
            'year': self.date.year
        })

    @property
    def image_size(self):
        return 'x{}'.format(500)
