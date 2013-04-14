import factory

from apps.artists.models import Artist
from ..exhibitions.related_factories import create_exhibitions
from ..press.related_factories import create_press
from ..photos.related_factories import create_photos


class ArtistFactory(factory.DjangoModelFactory):
    FACTORY_FOR = Artist

    first_name = factory.Sequence(lambda n: 'Firstname{}'.format(n))
    last_name = factory.Sequence(lambda n: 'Lastname{}'.format(n))
    visible = True

    photos = factory.PostGeneration(create_photos)
    exhibitions = factory.PostGeneration(create_exhibitions)
    press = factory.PostGeneration(create_press)
