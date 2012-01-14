import os

from django.db.models import permalink
from django.template.defaultfilters import slugify
from django.db import models

from canada.artists.models import Artist
from canada.exhibitions.models import Exhibition
from canada.functions import cap



class Press(models.Model):
    title = models.CharField(max_length=50)

    def image_path(instance, filename):
        return os.path.join('press', str(instance.press.date.year), str(instance.exhibition.slug), filename)
    image = models.ImageField(null=True, blank=True, upload_to=image_path)
    url = models.URLField(blank=True)
    date = models.DateField()

    publisher = models.CharField(max_length=60)
    author = models.CharField(max_length=60, blank=True)
    artists = models.ManyToManyField(Artist, blank=True, null=True)
    exhibition = models.ForeignKey(Exhibition, blank=True, null=True)

    slug = models.SlugField(blank=True, editable=False, unique=True)

    class Meta:
        ordering = ['-date']
        verbose_name_plural = "press"


    def __unicode__(self):
        return u'%s-%s-%s' % (self.publisher, self.date.year, self.title)

    def save(self):
        cap(self,'publisher', 'author')
        self.slug = slugify(self.title)
        super(Press, self).save()

    @permalink
    def get_absolute_url(self):
        return ('press.views.single', (), {
            'slug': self.slug,
            'year': self.date.strftime("%Y")
            })
