import collections
import datetime

import factory

from canada.apps.press.models import Press
from ..factories import DjangoFactory
from ..artists.factories import ArtistFactory


class PressFactory(DjangoFactory):
    FACTORY_FOR = Press

    link = factory.Sequence(lambda n: 'link{}.com'.format(n))
    title = factory.Sequence(lambda n: 'title{}'.format(n))
    publisher = factory.Sequence(lambda n: 'publisher{}'.format(n))
    date = datetime.date.today()

    @factory.post_generation(extract_prefix='artists')
    def create_artists(self, create, extracted, **kwargs):
        if isinstance(extracted, collections.Iterable):
            self.artists = extracted
        elif 'n' in kwargs:
            self.artists = [ArtistFactory() for _ in range(int(kwargs['n']))]
