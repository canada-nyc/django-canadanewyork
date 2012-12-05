import os

from markdown_deux.templatetags.markdown_deux_tags import markdown_allowed

from django.db.models import permalink
from django.db import models
from django.core.exceptions import ValidationError

from ..artists.models import Artist
from ..exhibitions.models import Exhibition
from libs.slugify.fields import SlugifyField
from libs.content_redirects.fields import RedirectField


class CompleteManager(models.Manager):
    def get_query_set(self):
        queryset = super(CompleteManager, self).get_query_set()
        return queryset.exclude(date__isnull=True)


class Press(models.Model):
    def image_path(instance, filename):
        return os.path.join('press',
                            str(instance.date.year),
                            instance.exhibition.slug,
                            filename)

    title = models.CharField(max_length=50)
    add_image = models.ImageField(
        null=True,
        blank=True,
        upload_to=image_path,
        help_text=('If an image is uploaded, it will be added to the pdf as '
                   'the next page of the pdf. If no pdf is attached to the '
                   'artist, one will be created using this image. So either '
                   'you can upoad a multipage pdf, or upload many images'
                   'one at a time that will be combined to make a multipage '
                   'pdf')
    )
    link = models.URLField(null=True, blank=True, verbose_name=u'External link')
    content = models.TextField(help_text=markdown_allowed(), blank=True)
    pdf = models.FileField(upload_to=image_path, blank=True, null=True)

    date = models.DateField(null=True,
                            help_text=('If the date is blank, then it will'
                                       ' be treated as a draft and not appear'
                                       ' on the site'))

    publisher = models.CharField(max_length=50, blank=True)
    author = models.CharField(max_length=60, blank=True)
    artists = models.ManyToManyField(Artist, blank=True, null=True,
                                     related_name='press',)
    exhibition = models.ForeignKey(Exhibition, blank=True, null=True,
                                   related_name='press',)
    slug = SlugifyField(populate_from=('title',))

    old_path = models.CharField(blank=True, null=True, editable=False, max_length=200)
    redirect = RedirectField()

    objects = CompleteManager()
    all_objects = models.Manager()

    class Meta:
        ordering = ['-date']
        verbose_name_plural = "press"

    def __unicode__(self):
        return u'{} ({})'.format(self.title, self.date.year)

    def clean(self):
        if self.pdf and self.pdf._file and self.pdf._file.content_type != 'application/pdf':
            file_type = self.pdf._file.content_type.split('/')[1]
            error = 'You uploaded a {}. A PDF is required'.format(file_type)
            raise ValidationError(error)

        self.title = self.title.strip().title()
        self.content = self.content.strip()
        self.publisher = self.publisher.strip().title()
        self.author = self.author.strip().title()

    @permalink
    def get_absolute_url(self):
        return ('press-detail', (), {
            'slug': self.slug,
            'year': self.date.year
        })
