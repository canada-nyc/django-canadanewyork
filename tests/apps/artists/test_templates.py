from django_webtest import WebTest

from .factories import ArtistFactory
from ..exhibitions.factories import ExhibitionFactory
from ..press.factories import PressFactory


class ArtistTest(WebTest):
    def test_visible(self):
        Artist = ArtistFactory(visible=True)
        artists_list = self.app.get('/artists/')
        assert Artist.__unicode__() in artists_list

        artist_detail = self.app.get(Artist.get_absolute_url())
        assert Artist.__unicode__() in artist_detail

    def test_invisible(self):
        Artist = ArtistFactory(visible=False)
        artists_list = self.app.get('/artists/')
        assert Artist.__unicode__() not in artists_list

        artists_list = self.app.get(Artist.get_absolute_url(), status=404)

    def test_related(self):
        Artist = ArtistFactory(
            visible=True,
        )
        Exhibition = ExhibitionFactory(artists=[Artist])
        PressArtist = PressFactory(artists=[Artist])
        PressExhibition = PressFactory(exhibition=Exhibition)
        artist_detail = self.app.get(Artist.get_absolute_url())
        press_list = artist_detail.click('Press')

        assert Exhibition.name in artist_detail
        assert PressArtist.title in press_list
        assert PressExhibition.title in press_list
        assert PressArtist.title in press_list.click(PressArtist.title)
        assert PressExhibition.title in press_list.click(PressExhibition.title)
