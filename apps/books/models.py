import urllib.parse

from django.db import models
from django.core.urlresolvers import reverse

from libs.ckeditor.fields import CKEditorField
import dumper

from ..artists.models import Artist


class Book(models.Model):
    title = models.CharField(max_length=500)
    artist = models.ForeignKey(Artist, related_name='books')
    description = CKEditorField(blank=True)

    date = models.DateField(
        verbose_name='Precise Date',
        help_text='Used for ordering'
    )
    date_text = models.CharField(
        verbose_name='Inprecise Date',
        max_length=500,
        blank=True,
        help_text="If set, will display <strong>instead of</strong> the precise date."
    )

    class Meta:
        ordering = ['-date']

    def __str__(self):
        return self.title

    def clean(self):
        self.title = self.title.strip().title()

    def get_absolute_url(self):
        return reverse('book-detail', kwargs={'pk': self.pk})

    @property
    def link_email(self):
        return 'gallery@canadanewyork.com'

    @property
    def link_subject(self):
        return 'Purchase Book'

    @property
    def link_body_template(self):
        return 'Hello\nI am interested in buying {first} {last}:{title}. Can you please contact me for pricing and availabilty?'

    @property
    def link_body(self):
        return self.link_body_template.format(
            first=self.artist.first_name,
            last=self.artist.last_name,
            title=self.title
        )

    def url_quote(self, string):
        return urllib.parse.quote(string, '')

    def get_purchase_url(self):
        arguments = [self.link_email, self.link_subject, self.link_body]
        return 'mailto:{}?subject={}&body={}'.format(
            *list(map(self.url_quote, arguments))
        )

    def dependent_paths(self):
        if self.artist:
            yield self.artist.get_absolute_url()
            yield reverse('artist-book-list', kwargs={'slug': self.artist.slug})
            yield reverse('book-list')

dumper.register(Book)
