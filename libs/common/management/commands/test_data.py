from django.core import management

from tests.apps.exhibitions.factories import ExhibitionFactory
from tests.apps.press.factories import PressFactory
from tests.apps.artists.factories import ArtistFactory
from tests.apps.updates.factories import UpdateFactory


class Command(management.base.BaseCommand):
    help = 'Adds some random test data'

    def handle(self, *args, **options):
        ArtistFactory(photos__n=3, visible=True)
        ExhibitionFactory(photos__n=3)
        PressFactory(artists__n=1)
        PressFactory(exhibition=ExhibitionFactory())
        UpdateFactory(photos__n=3)
