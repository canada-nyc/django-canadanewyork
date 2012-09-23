import datetime
import collections

import factory

from canada.apps.exhibitions.models import Exhibition, ExhibitionPhoto
from ..factories import DjangoFactory, BasePhotoFactory
from ..artists.factories import ArtistFactory


class ExhibitionFactory(DjangoFactory):
    FACTORY_FOR = Exhibition

    name = factory.Sequence(lambda n: 'name{}'.format(n))
    description = '*italics* **bold**'
    artists = [ArtistFactory()]

    start_date = datetime.date.today()
    end_date = datetime.date.today()

    @factory.post_generation(extract_prefix='photos')
    def create_photos(self, create, extracted, **kwargs):
        # ExhibitionFactory(photos__n=3)
        if 'n' in kwargs:
            [ExhibitionPhotoFactory(exhibition=self) for _ in range(int(kwargs['n']))]

    @factory.post_generation(extract_prefix='artists')
    def create_artists(self, create, extracted, **kwargs):
        # ExhibitionFactory(artists=[<artist1>, ...])
        if isinstance(extracted, collections.Iterable):
            self.artists = extracted
        # ExhibitionFactory(artists__n=3)
        elif 'n' in kwargs:
            self.artists = [ArtistFactory() for _ in range(int(kwargs['n']))]


class ExhibitionPhotoFactory(BasePhotoFactory):
    FACTORY_FOR = ExhibitionPhoto

    exhibition = factory.SubFactory(ExhibitionFactory)
