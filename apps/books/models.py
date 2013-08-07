import urllib

from django.db import models
from django.core.urlresolvers import reverse

import dumper

from ..artists.models import Artist


class Book(models.Model):
    title = models.CharField(max_length=500)
    date = models.DateField()
    artist = models.ForeignKey(Artist, related_name='books')

    class Meta:
        ordering = ['-date']

    def __unicode__(self):
        return self.title

    def clean(self):
        self.title = self.title.strip().title()

    @property
    def link_email(self):
        return u'gallery@canadanewyork.com'

    @property
    def link_subject(self):
        return u'Purchase Book'

    @property
    def link_body_template(self):
        return u'Hello\nI am interested in buying {first} {last}:{title}. Can you please contact me for pricing and availabilty?'

    @property
    def link_body(self):
        return self.link_body_template.format(
            first=self.artist.first_name,
            last=self.artist.last_name,
            title=self.title
        )

    def url_quote(self, string):
        return urllib.quote(string, '')

    def get_purchase_url(self):
        arguments = [self.link_email, self.link_subject, self.link_body]
        return u'mailto:{}?subject={}&body={}'.format(
            *map(self.url_quote, arguments)
        )

    def dependent_paths(self):
        if self.artist:
            yield self.artist.get_absolute_url()
            yield reverse('artist-book-list', kwargs={'slug': self.artist.slug})

dumper.register(Book)
