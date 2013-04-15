from django.test import TestCase

from .factories import PressFactory
from ..exhibitions.factories import ExhibitionFactory
from ..artists.factories import ArtistFactory


class PressFullTitleTest(TestCase):
    def test_blank(self):
        Press = PressFactory.create(title='')
        self.assertEquals('', Press.full_title)

    def test_title(self):
        Press = PressFactory(title='title')
        self.assertEquals(Press.title, Press.full_title)

    def test_exhibition(self):
        Exhibition = ExhibitionFactory.create()
        Press = PressFactory(exhibition=Exhibition, title='')
        self.assertEquals(unicode(Exhibition), Press.full_title)

    def test_artist(self):
        Artist = ArtistFactory.create()
        Press = PressFactory(artist=Artist, title='')
        self.assertEquals(unicode(Artist), Press.full_title)
