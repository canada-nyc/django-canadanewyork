from django.core import management

from tests.apps.bulkmail.factories import ContactListFactory
from tests.apps.exhibitions.factories import ExhibitionFactory
from tests.apps.info.factories import InfoFactory
from tests.apps.press.factories import PressFactory
from tests.apps.artists.factories import ArtistFactory
from tests.apps.updates.factories import UpdateFactory
from tests.apps.frontpage.factories import FrontpageFactory


class Command(management.base.BaseCommand):
    help = 'Adds some random test data'

    def handle(self, *args, **options):
        ArtistFactory(photos__n=3)
        ContactListFactory(contacts__n=3)
        ExhibitionFactory(photos__n=3)
        FrontpageFactory()
        InfoFactory()
        PressFactory(artists__n=3)
        PressFactory(exhibition=ExhibitionFactory())
        UpdateFactory(photos__n=3)
