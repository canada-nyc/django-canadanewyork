from django.core import management
from django.contrib.sites.models import Site

from tests.apps.bulkmail.factories import ContactListFactory
from tests.apps.exhibitions.factories import ExhibitionFactory
from tests.apps.info.factories import InfoFactory
from tests.apps.press.factories import PressFactory
from tests.apps.artists.factories import ArtistFactory
from tests.apps.updates.factories import UpdateFactory


class Command(management.base.BaseCommand):
    help = 'Adds some random test data'

    def handle(self, *args, **options):
        ArtistFactory(photos__n=3)
        ContactListFactory(contacts__n=3)
        ExhibitionFactory(photos__n=3)
        InfoFactory()
        PressFactory(artists__n=1)
        PressFactory(exhibition=ExhibitionFactory())
        UpdateFactory(photos__n=3)

        Site.objects.filter(id=1).update(domain='127.0.0.1:8000', name='localhost')
