import factory

from apps.exhibitions.models import Exhibition, ExhibitionPhoto
from ..artists.related_factories import create_artists
from ..press.related_factories import create_press
from ..photos.factories import get_create_function
from ... import utils


class ExhibitionFactory(factory.DjangoModelFactory):
    class Meta:
        model = Exhibition

    name = utils.FakerTitle()
    description = factory.Faker('text')
    extra_info = factory.Faker('text')
    current = False

    start_date = utils.FuzzyDate()
    end_date = factory.LazyAttribute(lambda obj: utils.random_date(start_date=obj.start_date))

    photos = factory.PostGeneration(get_create_function(ExhibitionPhoto))
    artists = factory.PostGeneration(create_artists)
    press = factory.PostGeneration(create_press)

    press_release_photo = utils.FakerImageField()
