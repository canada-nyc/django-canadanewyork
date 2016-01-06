from django.test import TestCase
from django.core.files.base import ContentFile

from .factories import ArtistFactory
from apps.artists.models import Artist
from ..exhibitions.factories import ExhibitionFactory
from ..press.factories import PressFactory


class ArtistVisibleTest(TestCase):

    def test_in_gallery(self):
        ArtistFactory.create(visible=True)

        assert Artist.in_gallery.exists()

    def test_not_in_gallery(self):
        ArtistFactory.create(visible=False)

        assert not Artist.in_gallery.exists()


class ArtistResumeTest(TestCase):

    def test_resume_file(self):
        Artist = ArtistFactory()
        Artist.resume_file.save('file.txt', ContentFile("my string content"))
        assert Artist.get_resume_url() == Artist.resume_file.url

    def test_resume(self):
        Artist = ArtistFactory(resume='_')

        assert Artist.get_resume_url() == Artist.get_resume_page_url()


class ArtistAllPressTest(TestCase):

    def setUp(self):
        self.ArtistPress = PressFactory.create(title='artist_press')
        self.ExhibitionPress = PressFactory.create(title='exhibition_press')

        self.Artist = ArtistFactory.create()
        self.Exhibition = ExhibitionFactory.create()
        self.Exhibition.artists.add(self.Artist)

    def test_no_press(self):
        assert not self.Artist.all_press.exists()

    def test_with_artist(self):
        self.ArtistPress.artist = self.Artist
        self.ArtistPress.save()
        assert self.Artist.all_press[0] == self.ArtistPress
        assert len(self.Artist.all_press) == 1

    def test_with_exhibition_with_artist(self):
        self.ExhibitionPress.exhibition = self.Exhibition
        self.ExhibitionPress.save()

        assert self.Artist.all_press[0] == self.ExhibitionPress
        assert len(self.Artist.all_press) == 1

    def test_with_artist_and_exhibition_with_artist(self):
        self.ExhibitionPress.exhibition = self.Exhibition
        self.ExhibitionPress.save()
        self.ArtistPress.artist = self.Artist
        self.ArtistPress.save()

        assert self.ExhibitionPress in self.Artist.all_press
        assert self.ArtistPress in self.Artist.all_press
        assert self.Artist.all_press.count() == 2
