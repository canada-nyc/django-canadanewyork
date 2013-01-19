from django.db import models
from django.db.models import permalink
from django.contrib.contenttypes import generic

from markdown_deux.templatetags.markdown_deux_tags import markdown_allowed

from libs.update_related.models import RedirectField
from libs.common.models import Photo


class Update(models.Model):
    description = models.TextField(blank=True, null=True,
                                   help_text=markdown_allowed())
    post_date = models.DateTimeField(auto_now_add=True)

    old_path = models.CharField(blank=True, null=True, editable=False, max_length=2000)
    redirect = RedirectField()

    photos = generic.GenericRelation(Photo)

    class Meta:
        ordering = ["-post_date"]

    def clean(self):
        self.description = self.description.strip()

    def __unicode__(self):
        return unicode('{} ({})').format(self.pk, self.post_date.year)

    @permalink
    def get_absolute_url(self):
        return ('update-single', (), {
            'pk': self.pk,
        })
