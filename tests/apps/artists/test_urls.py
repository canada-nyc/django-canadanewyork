from django.test import TestCase
from django.core.urlresolvers import reverse

from .factories import ArtistFactory


class ArtistUrlTest(TestCase):
    def test_detail(self):
        Artist = ArtistFactory.create()
        assert Artist.get_absolute_url() == reverse('artist-detail', kwargs={'slug': Artist.slug})
