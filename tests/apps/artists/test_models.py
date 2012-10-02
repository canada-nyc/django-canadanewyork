from django.test import TestCase

from .factories import ArtistFactory


class ArtistTest(TestCase):
    def test_create_artist(self):
        artist = ArtistFactory(photos__n=1)
