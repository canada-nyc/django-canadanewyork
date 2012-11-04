import os

from django.db import models
from django.db.models import permalink

from markdown_deux.templatetags.markdown_deux_tags import markdown_allowed

from ..common.models import BasePhoto
from ..slugify.fields import SlugifyField


class Update(models.Model):

    name = models.CharField(max_length=30, unique_for_year='post_date')
    description = models.TextField(blank=True, null=True,
                                   help_text=markdown_allowed())
    post_date = models.DateTimeField(auto_now_add=True)
    slug = SlugifyField(populate_from=(lambda U: U.post_date.year, 'name'))

    class Meta:
        ordering = ["-post_date"]

    def __unicode__(self):
        return '{} ({})'.format(self.name, self.post_date.year)

    @permalink
    def get_absolute_url(self):
        return ('update-single', (), {
            'slug': self.slug,
        })


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
