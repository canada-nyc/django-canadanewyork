import os

from markdown_deux.templatetags.markdown_deux_tags import markdown_allowed

from django.core.urlresolvers import reverse
from django.db import models
from django.core.exceptions import ValidationError

from ..artists.models import Artist
from ..exhibitions.models import Exhibition
from libs.slugify.fields import SlugifyField
from libs.content_redirects.fields import RedirectField
from libs.pdf_image_append.models import PDFImageAppendModel


class Press(models.Model, PDFImageAppendModel):
    def image_path(instance, filename):
        return os.path.join(instance.get_absolute_url()[1:], 'pdf', filename)

    title = models.CharField(max_length=500, unique_for_year='date')
    link = models.URLField(null=True, blank=True, verbose_name=u'External link')
    content = models.TextField(help_text=markdown_allowed(), blank=True)
    pdf = models.FileField(upload_to=image_path, blank=True, null=True, max_length=500)

    date = models.DateField()

    publisher = models.CharField(max_length=50, blank=True)
    author = models.CharField(max_length=60, blank=True)
    artists = models.ManyToManyField(Artist, blank=True, null=True,
                                     related_name='press',)
    exhibition = models.ForeignKey(Exhibition, blank=True, null=True,
                                   related_name='press',)
    slug = SlugifyField(populate_from=('title',))

    old_path = models.CharField(blank=True, null=True, editable=False, max_length=2000)
    redirect = RedirectField()

    class Meta:
        ordering = ['-date']
        verbose_name_plural = "press"

    def __unicode__(self):
        return u'{} ({})'.format(self.title, getattr(self.date, 'year', None))

    def clean(self):
        if self.pdf and self.pdf._file and self.pdf._file.content_type != 'application/pdf':
            file_type = self.pdf._file.content_type.split('/')[1]
            error = 'You uploaded a {}. A PDF is required'.format(file_type)
            raise ValidationError(error)

        self.title = self.title.strip().title()
        self.content = self.content.strip()
        self.publisher = self.publisher.strip().title()
        self.author = self.author.strip().title()

    def get_absolute_url(self):
        return reverse('press-detail', kwargs={
            'slug': self.slug,
            'year': self.date.year
        })
