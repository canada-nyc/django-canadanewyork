import factory

from apps.artists.models import Artist, ArtistPhoto
from ..exhibitions.related_factories import create_exhibitions
from ..press.related_factories import create_press
from ..photos.factories import get_create_function
from ..books.related_factories import create_books


class ArtistFactory(factory.DjangoModelFactory):
    class Meta:
        model = Artist

    first_name = factory.Faker('first_name')
    last_name = factory.Faker('last_name')
    website = factory.Faker('url')
    resume = factory.Faker('text')
    visible = True

    photos = factory.PostGeneration(get_create_function(ArtistPhoto))
    exhibitions = factory.PostGeneration(create_exhibitions)
    press = factory.PostGeneration(create_press)
    books = factory.PostGeneration(create_books)
