import os

from markdown_deux.templatetags.markdown_deux_tags import markdown_allowed

from django.core.urlresolvers import reverse
from django.db import models

from ..artists.models import Artist
from ..exhibitions.models import Exhibition
from libs.slugify.fields import SlugifyField
from libs.update_related.models import RedirectField


class Press(models.Model):
    def image_path(instance, filename):
        return os.path.join(instance.get_absolute_url()[1:], 'content', filename)

    title = models.CharField(max_length=500)
    link = models.URLField(null=True, blank=True, verbose_name=u'External link')
    content = models.TextField(help_text=markdown_allowed(), blank=True)
    content_file = models.FileField(upload_to=image_path, blank=True, null=True, max_length=500)

    date = models.DateField()

    publisher = models.CharField(max_length=50, blank=True)
    author = models.CharField(max_length=60, blank=True)
    artists = models.ManyToManyField(Artist, blank=True, null=True,
                                     related_name='press',)
    exhibition = models.ForeignKey(Exhibition, blank=True, null=True,
                                   related_name='press',)
    slug = SlugifyField(populate_from=('publisher', 'title',), unique_for_year='date')

    old_path = models.CharField(blank=True, null=True, editable=False, max_length=2000)
    redirect = RedirectField()

    old_content_path = models.CharField(blank=True, max_length=1000)
    image_redirect = RedirectField(model_to_related={
        'old_path': lambda model: model.old_content_path,
        'new_path': lambda model: model.content_file and model.content_file.url,
    }, related_name='press_images')

    class Meta:
        ordering = ['-date']
        verbose_name_plural = "press"

    def __unicode__(self):
        return u'{} ({})'.format(self.title, getattr(self.date, 'year', None))

    def clean(self):

        self.title = self.title.strip().title()
        self.content = self.content.strip()
        self.publisher = self.publisher.strip().title()
        self.author = self.author.strip().title()

    def get_absolute_url(self):
        return reverse('press-detail', kwargs={
            'slug': self.slug,
            'year': self.date.year
        })
