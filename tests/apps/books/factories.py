import factory

from apps.books.models import Book
from ..artists.factories import ArtistFactory
from ... import utils


class BookFactory(factory.DjangoModelFactory):

    FACTORY_FOR = Book

    title = factory.Sequence(lambda n: 'title{}'.format(n))
    date = utils.FuzzyDate()

    artist = factory.SubFactory(ArtistFactory)
