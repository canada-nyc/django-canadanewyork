import factory

from django.core import management

from tests.apps.exhibitions.factories import ExhibitionFactory
from tests.apps.press.factories import PressFactory
from tests.apps.artists.factories import ArtistFactory
from tests.apps.updates.factories import UpdateFactory


class Command(management.base.BaseCommand):
    help = 'Adds some random test data'

    def handle(self, *args, **options):
        factory.create_batch(
            ArtistFactory,
            5,
            photos__n=3,
            exhibitions__n=1,
            exhibitions__photos__n=3,
            press__n=2,
            press__content='content_in_press',
            books__n=4,
            books__photos__n=1,
        )
        PressFactory(artist__n=1, content_file__make=True)
        ExhibitionFactory(press__n=3, press__content_file__make=True,
                          photos__n=4)
        factory.create_batch(
            UpdateFactory,
            5,
            photos__n=3,
            description=' update description!'
        )
