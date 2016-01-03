import factory

from apps.books.models import Book
from ..artists.factories import ArtistFactory
from ... import utils


class BookFactory(factory.DjangoModelFactory):

    class Meta:
        model = Book

    title = factory.Sequence(lambda n: 'title{}'.format(n))
    date = utils.FuzzyDate()

    description = factory.Faker('text')

    artist = factory.SubFactory(ArtistFactory)
