import factory

from apps.artists.models import Artist, ArtistPhoto
from ..exhibitions.related_factories import create_exhibitions
from ..press.related_factories import create_press
from ..photos.factories import get_create_function
from ..books.related_factories import create_books


class ArtistFactory(factory.DjangoModelFactory):
    class Meta:
        model = Artist

    first_name = factory.Sequence(lambda n: 'Firstname{}'.format(n))
    last_name = factory.Sequence(lambda n: 'Lastname{}'.format(n))
    visible = True

    photos = factory.PostGeneration(get_create_function(ArtistPhoto))
    exhibitions = factory.PostGeneration(create_exhibitions)
    press = factory.PostGeneration(create_press)
    books = factory.PostGeneration(create_books)
