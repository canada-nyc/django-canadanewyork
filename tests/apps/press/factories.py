import factory

from apps.press.models import Press
from ..artists.related_factories import create_artist
from ..exhibitions.related_factories import create_exhibition
from ... import utils


class PressFactory(factory.DjangoModelFactory):
    class Meta:
        model = Press

    title = factory.Sequence(lambda n: 'title{}'.format(n))
    date = utils.FuzzyDate()

    exhibition = factory.PostGeneration(create_exhibition)
    artist = factory.PostGeneration(create_artist)

    content_file = factory.django.FileField()
