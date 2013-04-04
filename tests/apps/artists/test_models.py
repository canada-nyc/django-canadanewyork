from django.test import TestCase

from .factories import ArtistFactory


class ArtistTest(TestCase):
    def test_create_artist(self):
        artist = ArtistFactory()
        self.assertTrue(artist)
