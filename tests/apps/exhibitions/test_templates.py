from django_webtest import WebTest

from .factories import ExhibitionFactory
from ..artists.factories import ArtistFactory
from ..press.factories import PressFactory


class ExhibitionTest(WebTest):

    def test_list(self):
        Exhibition = ExhibitionFactory()
        exhibition_list = self.app.get('/exhibitions/')
        assert Exhibition.name in exhibition_list
        assert self.app.get(Exhibition.get_absolute_url()).content == exhibition_list.click(Exhibition.name).content

    def test_detail(self):
        Exhibition = ExhibitionFactory()
        exhibition_detail = self.app.get(Exhibition.get_absolute_url())
        assert Exhibition.name in exhibition_detail

    def test_related(self):
        Artist = ArtistFactory()
        Exhibition = ExhibitionFactory(
            artists=[Artist]
        )
        Press = PressFactory(exhibition=Exhibition)
        exhibition_detail = self.app.get(Exhibition.get_absolute_url())
        press_list = exhibition_detail.click('Press')

        assert Artist.__unicode__() in exhibition_detail
        assert Press.title in press_list
        assert Press.title in press_list.click(Press.title)
