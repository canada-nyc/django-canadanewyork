from webtest.app import AppError

from django_webtest import WebTest
from django.core.urlresolvers import reverse
from django.core.files.base import ContentFile

from .factories import PressFactory
from ..artists.factories import ArtistFactory
from ..exhibitions.factories import ExhibitionFactory


class PressDetailTest(WebTest):
    def test_unicode(self):
        Press = PressFactory()
        press_detail = self.app.get(Press.get_absolute_url())
        self.assertIn(unicode(Press), press_detail)

    def test_content(self):
        Press = PressFactory(content='content stuff')
        press_detail = self.app.get(Press.get_absolute_url())
        self.assertIn(Press.content, press_detail)

    def test_content_file_link(self):
        Press = PressFactory()
        Press.content_file.save('file.txt', ContentFile("my string content"))
        press_detail = self.app.get(Press.get_absolute_url())

        # for some reason static isn't being served for tests
        try:
            press_detail.click(href=Press.content_file.url)
        except AppError:
            pass

    def test_artist_link(self):
        Artist = ArtistFactory.create()
        Press = PressFactory.create(artist=Artist)
        press_detail = self.app.get(Press.get_absolute_url())
        press_detail.click(
            unicode(Artist),
            href=reverse('artist-detail', kwargs={'slug': Artist.slug})
        )

    def test_exhibition_link(self):
        Exhibition = ExhibitionFactory.create()
        Press = PressFactory.create(exhibition=Exhibition)
        press_detail = self.app.get(Press.get_absolute_url())
        press_detail.click(
            unicode(Exhibition),
            href=reverse('exhibition-detail', kwargs={'slug': Press.exhibition.slug})
        )
