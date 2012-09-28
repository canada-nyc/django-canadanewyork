from django.test import TestCase

from .factories import ExhibitionFactory


class ExhibitionTest(TestCase):
    def test_create_exhibition(self):
        ExhibitionFactory(photos__n=1, artists=0)
        ExhibitionFactory()
        ExhibitionFactory(artists=3)
