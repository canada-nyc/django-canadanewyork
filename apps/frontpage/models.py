import os

from django.db import models
from django.db.models import permalink

from smart_selects.db_fields import ChainedForeignKey
from markdown_deux.templatetags.markdown_deux_tags import markdown_allowed


from ..exhibitions.models import Exhibition
from ..unique_boolean.fields import UniqueBooleanField
from ..common.models import Photo


class Frontpage(models.Model):
    def image_path(instance, filename):
        return os.path.join(
            'frontpage',
            str(instance.date_added),
            filename)
    date_added = models.DateField(auto_now_add=True)
    activated = UniqueBooleanField(
        verbose_name='Use as frontpage?',
        help_text="To switch frontpages, activate a different one",
        default=True)
    uploaded_image = models.ImageField(
        upload_to=image_path,
        help_text='Uploaded image will <strong>override</strong> selected image',
        blank=True,
        null=True)

    extra_text = models.TextField(
        max_length=800,
        help_text=('Will be added underneath any exhibition info<br>' +
                   markdown_allowed()),
        blank=True,
        null=True,
    )
    exhibition = models.ForeignKey(Exhibition, blank=True, null=True)
    exhibition_image = ChainedForeignKey(
        Photo,
        chained_model_field='content_object',
        chained_field='exhibition',
        help_text=('Select exhibition first, then choose an image from that'
                   ' exhibition. If an uploaded image is selected, that will'
                   ' take precedence'),
        show_all=False,
        blank=True,
        null=True,
    )

    class Meta:
        ordering = ["-date_added"]

    def __unicode__(self):
        return str(self.date_added)

    def clean(self):
        self.extra_text = self.extra_text.strip()

    @permalink
    def get_absolute_url(self):
        return ('frontpage-detail', (), {'pk': self.pk})

    def image(self):
        if self.uploaded_image:
            return self.uploaded_image
        elif self.exhibition_image:
            return self.exhibition_image.image
