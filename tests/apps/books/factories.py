import factory

from apps.books.models import Book, BookPhoto
from ..artists.factories import ArtistFactory
from ..photos.factories import get_create_function
from ... import utils


class BookFactory(factory.DjangoModelFactory):

    class Meta:
        model = Book

    title = utils.FakerTitle()
    date = utils.FuzzyDate()
    price = factory.fuzzy.FuzzyInteger(1, 100)

    description = factory.Faker('text')

    artist = factory.SubFactory(ArtistFactory)
    photos = factory.PostGeneration(get_create_function(BookPhoto))
