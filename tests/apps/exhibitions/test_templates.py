from django_webtest import WebTest

from apps.exhibitions.models import Exhibition
from .factories import ExhibitionFactory
from ..artists.factories import ArtistFactory
from ..press.factories import PressFactory


class ExhibitionTest(WebTest):

    def test_list(self):
        _Exhibition = ExhibitionFactory()
        exhibition_list = self.app.get('/exhibitions/')
        assert _Exhibition.name in exhibition_list
        assert self.app.get(_Exhibition.get_absolute_url()).content == exhibition_list.click(_Exhibition.name).content

    def test_detail(self):
        _Exhibition = ExhibitionFactory()
        exhibition_detail = self.app.get(_Exhibition.get_absolute_url())
        assert _Exhibition.name in exhibition_detail

    def test_related(self):
        Artist = ArtistFactory()
        _Exhibition = ExhibitionFactory(
            artists=[Artist]
        )
        Press = PressFactory(exhibition=_Exhibition)
        exhibition_detail = self.app.get(_Exhibition.get_absolute_url())
        press_list = exhibition_detail.click('Press')

        assert Artist.__unicode__() in exhibition_detail
        assert Press.title in press_list
        assert Press.title in press_list.click(Press.title)

    def test_current(self):
        ExhibitionFactory()
        current = Exhibition.objects.get(current=True)
        exhibition_current = self.app.get('/')
        exhibition_detail = exhibition_current.click(current.name)
        assert exhibition_detail.content == self.app.get(current.get_absolute_url()).content
