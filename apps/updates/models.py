from django.db import models
from django.db.models import permalink
from django.contrib.contenttypes import generic

from markdown_deux.templatetags.markdown_deux_tags import markdown_allowed

from ..slugify.fields import SlugifyField
from ..content_redirects.models import BaseRedirectModel
from ..common.models import Photo


class Update(BaseRedirectModel):
    name = models.CharField(max_length=30, unique_for_year='post_date')
    description = models.TextField(blank=True, null=True,
                                   help_text=markdown_allowed())
    post_date = models.DateTimeField(auto_now_add=True)
    slug = SlugifyField(populate_from=(lambda U: U.post_date.year, 'name'))

    photos = generic.GenericRelation(Photo)

    class Meta:
        ordering = ["-post_date"]

    def __unicode__(self):
        return '{} ({})'.format(self.name, self.post_date.year)

    @permalink
    def get_absolute_url(self):
        return ('update-single', (), {
            'slug': self.slug,
        })
