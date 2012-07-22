import os

from django.db import models
from django.db.models import permalink
from django.core.exceptions import ValidationError

from smart_selects.db_fields import ChainedForeignKey

from ..exhibitions.models import Exhibition, ExhibitionPhoto
from ..updates.models import Update, UpdatePhoto


class Frontpage(models.Model):
    def image_path(instance, filename):
        return os.path.join(
            'frontpage',
            str(instance.date_added),
            filename
        )
    custom_title = models.CharField(
        max_length=40,
        null=True,
        blank=True,
        verbose_name='Title',
        help_text=('Will override the exhibition or update title, if either are'
                   ' selected')
    )
    date_added = models.DateField(auto_now_add=True)
    activated = models.BooleanField(
        verbose_name='Use as frontpage?',
        help_text="To switch frontpages, activate a different one"
    )
    uploaded_image = models.ImageField(
        upload_to=image_path,
        help_text='Uploaded image will <strong>override</strong> selected image',
        blank=True,
        null=True
    )

    text = models.TextField(
        max_length=800,
        help_text=('Will be added underneath any exhibition or update info<br>'
                   '<em>To add style:</em> use markdown('
                   '<a href="http://daringfireball.net/projects/markdown/basics"'
                   ' target="_blank">reference</a>)'),
        blank=True,
        null=True,
    )
    exhibition = models.ForeignKey(Exhibition, blank=True, null=True)
    exhibition_image = ChainedForeignKey(
        ExhibitionPhoto,
        chained_model_field='exhibition',
        chained_field='exhibition',
        verbose_name='Select image from exhibition',
        help_text=('Select exhibition first, then choose an image from that'
                   ' exhibition. If an uploaded image is selected, that will'
                   ' take precedence'),
        blank=True,
        null=True,
    )
    exhibition_text = models.BooleanField(
        verbose_name='Include exhibition description?',
        default=True
    )
    update = models.ForeignKey(Update, blank=True, null=True)
    update_image = ChainedForeignKey(
        UpdatePhoto,
        chained_model_field='update',
        chained_field='update',
        verbose_name='Select image from update',
        help_text=('Select update first, then choose an image from that'
                 ' update. If an uploaded image is selected, that will'
                 ' take precedence'),
        blank=True,
        null=True,
    )
    update_text = models.BooleanField(
        verbose_name='Include update description?',
        default=True
    )

    class Meta:
        ordering = ["-date_added"]

    def __unicode__(self):
        return str(self.date_added)

    def save(self, *args, **kwargs):
        if self.activated:
            Frontpage.objects.all().update(activated=False)
        elif not Frontpage.objects.filter(activated=True).exists():
            self.activated = True

        if not self.exhibition:
            self.exhibition_text = False
        if not self.update:
            self.update_text = False
        super(Frontpage, self).save(*args, **kwargs)

    @permalink
    def get_absolute_url(self):
        return ('frontpage-detail', (), {'pk': self.pk})

    def clean(self):
        if self.exhibition and self.update:
            raise ValidationError('An exhibition and an update can not both be'
                                  ' linked to the frontpage.')

    def image(self):
        if self.uploaded_image:
            return self.uploaded_image
        elif self.exhibition and self.exhibition_image:
            return self.exhibition_image.image
        elif self.update and self.update_image:
            return self.update_image.image

    def foreign_text(self):
        if self.exhibition_text and self.exhibition:
            if self.exhibition.description:
                return self.exhibition.description
        elif self.update_text and self.update:
            if self.update.description:
                return self.update.description
        else:
            return ''

    def title(self):
        if self.custom_title:
            return self.custom_title
        if self.exhibition:
            return self.exhibition.name
        elif self.update:
            return self.update.name
        else:
            return ''

    def url(self):
        if self.exhibition:
            return self.exhibition.get_absolute_url()
        elif self.update:
            return self.update.get_absolute_url()
