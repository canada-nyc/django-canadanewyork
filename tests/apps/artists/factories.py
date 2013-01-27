import factory

from apps.artists.models import Artist
from ...common.factories import DjangoFactory, BasePhotoFactory
from ...common.functions import django_pdf


class ArtistFactory(DjangoFactory):
    FACTORY_FOR = Artist

    first_name = factory.Sequence(lambda n: 'Firstname{}'.format(n))
    last_name = factory.Sequence(lambda n: 'Lastname{}'.format(n))
    resume = 'Really long resume. Has lots of _markdown_'

    resume = factory.Sequence(lambda n: django_pdf(n))

    @factory.post_generation(extract_prefix='photos')
    def create_photos(self, create, extracted, **kwargs):
        # ArtistFactory(photos__n=3)
        if 'n' in kwargs:
            [ArtistPhotoFactory(content_object=self) for _ in range(int(kwargs['n']))]


class ArtistPhotoFactory(BasePhotoFactory):
    content_object = factory.SubFactory(ArtistFactory)
