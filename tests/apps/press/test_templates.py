from django_webtest import WebTest
from django.core.urlresolvers import reverse
from django.core.files.base import ContentFile

from .factories import PressFactory
from ..artists.factories import ArtistFactory
from ..exhibitions.factories import ExhibitionFactory


class PressListTest(WebTest):
    def test_reverse(self):
        self.app.get(
            reverse('press-list')
        )

    def test_nav_click(self):
        press_list = self.app.get(
            reverse('press-list')
        )
        press_list.click(
            'Press',
            reverse('press-list')
        )

    def test_click_press(self):
        Press = PressFactory()
        press_list = self.app.get(
            reverse('press-list')
        )
        press_list.click(
            unicode(Press),
            reverse('press-detail', kwargs={'slug': Press.slug, })
        )


class PressDetailTest(WebTest):
    def test_unicode(self):
        Press = PressFactory()
        press_detail = self.app.get(Press.get_absolute_url())
        self.assertIn(unicode(Press), press_detail)

    def test_external_link(self):
        Press = PressFactory(link='http://some_site.com')
        press_detail = self.app.get(Press.get_absolute_url())
        press_detail.click(href=Press.link)

    def test_content_file_link(self):
        Press = PressFactory()
        Press.content_file.save('file.txt', ContentFile("my string content"))
        press_detail = self.app.get(Press.get_absolute_url())
        print press_detail
        press_detail.click(href=Press.content_file.url)

    def test_artist_link(self):
        Artist = ArtistFactory.create()
        Press = PressFactory.create(artist=Artist)
        press_detail = self.app.get(Press.get_absolute_url())
        press_detail.click(
            href=reverse('artist-detail', kwargs={'slug': Artist.slug})
        )

    def test_exhibition_link(self):
        Exhibition = ExhibitionFactory.create()
        Press = PressFactory.create(exhibition=Exhibition)
        press_detail = self.app.get(Press.get_absolute_url())
        press_detail.click(
            href=reverse('exhibition-detail', kwargs={'slug': Press.exhibition.slug})
        )
