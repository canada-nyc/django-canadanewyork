import os

from markdown_deux.templatetags.markdown_deux_tags import markdown_allowed

from django.db.models import permalink
from django.db import models

from ..artists.models import Artist
from ..exhibitions.models import Exhibition
from ..slugify.fields import SlugifyField
from ..content_redirects.models import BaseRedirectModel


class CompleteManager(models.Manager):
    def get_query_set(self):
        queryset = super(CompleteManager, self).get_query_set()
        return queryset.exclude(date__isnull=True)


class Press(BaseRedirectModel):
    def image_path(instance, filename):
        return os.path.join('press',
                            str(instance.date.year),
                            instance.exhibition.slug,
                            filename)

    title = models.CharField(max_length=50)
    image = models.ImageField(null=True, blank=True, upload_to=image_path)
    link = models.URLField(null=True, blank=True, verbose_name=u'External link')
    content = models.TextField(help_text=markdown_allowed())
    date = models.DateField(null=True,
                            help_text=('If the date is blank, then it will'
                                       ' be treated as a draft and not appear'
                                       ' on the site'))

    publisher = models.CharField(max_length=50, blank=True)
    author = models.CharField(max_length=60, blank=True, null=True)
    artists = models.ManyToManyField(Artist, blank=True, null=True,
                                     related_name='press',)
    exhibition = models.ForeignKey(Exhibition, blank=True, null=True,
                                   related_name='press',)
    slug = SlugifyField(populate_from=('title',))

    objects = CompleteManager()
    all_objects = models.Manager()

    class Meta:
        ordering = ['-date']
        verbose_name_plural = "press"

    def __unicode__(self):
        return u'{} ({})'.format(self.title, self.date.year)

    def clean(self):
        self.title = self.title.strip().title()
        self.content = self.content.strip()
        self.publisher = self.publisher.strip().title()
        self.author = self.author.strip.title()

    @permalink
    def get_absolute_url(self):
        return ('press-detail', (), {
            'slug': self.slug,
            'year': self.date.year
        })

