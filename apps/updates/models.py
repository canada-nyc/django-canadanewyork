from django.db import models
from django.db.models import permalink
from django.contrib.contenttypes import generic

from markdown_deux.templatetags.markdown_deux_tags import markdown_allowed

from libs.slugify.fields import SlugifyField
from libs.content_redirects.fields import RedirectField
from libs.common.models import Photo


class Update(models.Model):
    name = models.CharField(max_length=800, unique_for_year='post_date')
    description = models.TextField(blank=True, null=True,
                                   help_text=markdown_allowed())
    post_date = models.DateTimeField(auto_now_add=True)
    slug = SlugifyField(populate_from=(lambda U: U.post_date.year, 'name'))

    old_path = models.CharField(blank=True, null=True, editable=False, max_length=200)
    redirect = RedirectField()

    photos = generic.GenericRelation(Photo)

    class Meta:
        ordering = ["-post_date"]

    def clean(self):
        self.name = self.name.strip()
        self.description = self.description.strip()

    def __unicode__(self):
        return '{} ({})'.format(self.name, self.post_date.year)

    @permalink
    def get_absolute_url(self):
        return ('update-single', (), {
            'slug': self.slug,
        })
