import factory

from django.core.files.base import ContentFile

from apps.press.models import Press
from ..artists.related_factories import create_artist
from ..exhibitions.related_factories import create_exhibition
from ... import utils


class PressFactory(factory.DjangoModelFactory):

    FACTORY_FOR = Press

    title = factory.Sequence(lambda n: 'title{}'.format(n))
    date = utils.FuzzyDate()

    exhibition = factory.PostGeneration(create_exhibition)
    artist = factory.PostGeneration(create_artist)

    @factory.post_generation
    def content_file(self, create, extracted, **kwargs):
        if extracted:
            file_name, file = extracted
        elif kwargs.pop('make', None):
            file_name = 'image.jpg'
            file = ContentFile('Some file stuff')
        else:
            return
        self.content_file.save(file_name, file)
