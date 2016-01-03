import factory

from apps.books.models import Book, BookPhoto
from ..artists.factories import ArtistFactory
from ..photos.factories import get_create_function
from ... import utils


class BookFactory(factory.DjangoModelFactory):

    class Meta:
        model = Book

    title = factory.Sequence(lambda n: 'title{}'.format(n))
    date = utils.FuzzyDate()

    description = factory.Faker('text')

    artist = factory.SubFactory(ArtistFactory)
    photos = factory.PostGeneration(get_create_function(BookPhoto))
