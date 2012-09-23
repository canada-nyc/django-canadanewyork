import factory

from canada.apps.artists.models import Artist, ArtistPhoto
from ..factories import DjangoFactory, BasePhotoFactory
from ..functions import django_pdf


class ArtistFactory(DjangoFactory):
    FACTORY_FOR = Artist

    first_name = factory.Sequence(lambda n: 'Firstname{}'.format(n))
    last_name = factory.Sequence(lambda n: 'Lastname{}'.format(n))

    resume = factory.Sequence(lambda n: django_pdf(n, 'Ima s World'))

    @factory.post_generation(extract_prefix='photos')
    def create_photos(self, create, extracted, **kwargs):
        # ArtistFactory(photos__n=3)
        if 'n' in kwargs:
            [ArtistPhotoFactory(artist=self) for _ in range(int(kwargs['n']))]


class ArtistPhotoFactory(BasePhotoFactory):
    FACTORY_FOR = ArtistPhoto

    artist = factory.SubFactory(ArtistFactory)
