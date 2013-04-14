from django.test import TestCase
from django.core.urlresolvers import reverse

from .factories import ArtistFactory


class ArtistURLTest(TestCase):
    def test_detail(self):
        Artist = ArtistFactory.create()
        self.assertEqual(
            Artist.get_absolute_url(),
            reverse('artist-detail', kwargs={'slug': Artist.slug})
        )
