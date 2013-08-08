import factory

from apps.books.models import Book
from ..artists.factories import ArtistFactory


class BookFactory(factory.DjangoModelFactory):

    FACTORY_FOR = Book

    title = factory.Sequence(lambda n: 'title{}'.format(n))
    year = factory.Sequence(lambda n: n)

    artist = factory.SubFactory(ArtistFactory)
