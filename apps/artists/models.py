import os

from django.db import models
from django.db.models import permalink
from django.template.defaultfilters import slugify
from django.core.exceptions import ValidationError
from django.db.models import Q

from ..common.models import BasePhoto


class VisibleManager(models.Manager):
    def get_query_set(self):
        return super(VisibleManager, self).get_query_set().filter(visible=True)


class Artist(models.Model):
    def image_path(instance, filename):
        return os.path.join('artists',
                            instance.slug,
                            filename)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    resume = models.FileField(upload_to=image_path, blank=True, editable=False)
    slug = models.SlugField(blank=True, editable=False)
    visible = models.BooleanField(
        default=True,
        help_text="Whether it appears in the Artists list, and has page")
    objects = models.Manager()
    in_gallery = VisibleManager()

    class Meta:
        ordering = ['last_name', 'first_name']
        unique_together = ("first_name", "last_name")

    def __unicode__(self):
        return ' '.join([self.first_name, self.last_name])

    def save(self, *args, **kwargs):
        self.slug = slugify('-'.join([self.first_name, self.last_name]))
        super(Artist, self).save(*args, **kwargs)

    def clean(self):
        if self.resume and self.resume._file and self.resume._file.content_type != 'application/pdf':
            file_type = self.resume._file.content_type.split('/')[1]
            error = 'You uploaded a {}. A PDF is required'.format(file_type)
            raise ValidationError(error)

    @permalink
    def get_absolute_url(self):
        return ('artist-detail', (), {'slug': self.slug})

    def get_press(self):
        from ..press.models import Press
        return Press.objects.filter(Q(artists__in=[self]) |
                                    Q(exhibition__artists__in=[self]))

    @permalink
    def get_press_url(self):
        return ('artist-press-list', (), {
            'slug': self.slug
        })


class ArtistPhoto(BasePhoto):
    def image_path(instance, filename):
        return os.path.join('artists', instance.artist.slug, filename)

    artist = models.ForeignKey(Artist, related_name='images')
    image = models.ImageField(upload_to=image_path)

    def __unicode__(self):
            return u'{} by {}'.format(self.title, self.artist)