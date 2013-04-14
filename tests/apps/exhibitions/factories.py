import datetime

import factory

from apps.exhibitions.models import Exhibition
from ..artists.related_factories import create_artists
from ..press.related_factories import create_press
from ..photos.related_factories import create_photos


class ExhibitionFactory(factory.DjangoModelFactory):
    FACTORY_FOR = Exhibition

    name = factory.Sequence(lambda n: 'name{}'.format(n))

    start_date = datetime.date.today()
    end_date = datetime.date.today()

    photos = factory.PostGeneration(create_photos)
    artists = factory.PostGeneration(create_artists)
    press = factory.PostGeneration(create_press)
