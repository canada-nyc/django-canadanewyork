import factory

from apps.press.models import Press
from ..artists.related_factories import create_artist
from ..exhibitions.related_factories import create_exhibition
from ... import utils


class PressFactory(factory.DjangoModelFactory):
    class Meta:
        model = Press

    title = factory.Faker('word')
    content = factory.Faker('text')
    publisher = factory.Faker('company')
    publisher = factory.Faker('name')
    date = utils.FuzzyDate()

    exhibition = factory.PostGeneration(create_exhibition)
    artist = factory.PostGeneration(create_artist)

    content_file = factory.django.FileField()
