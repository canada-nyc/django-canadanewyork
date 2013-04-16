import factory

from apps.exhibitions.models import Exhibition
from ..artists.related_factories import create_artists
from ..press.related_factories import create_press
from ..photos.related_factories import create_photos
from ... import utils


class ExhibitionFactory(factory.DjangoModelFactory):
    FACTORY_FOR = Exhibition

    name = factory.Sequence(lambda n: 'name{}'.format(n))

    start_date = utils.FuzzyDate()
    end_date = factory.LazyAttribute(lambda obj: utils.random_date(start_date=obj.start_date))

    photos = factory.PostGeneration(create_photos)
    artists = factory.PostGeneration(create_artists)
    press = factory.PostGeneration(create_press)

    @factory.post_generation
    def press_release_photo(self, create, extracted, **kwargs):
        if extracted:
            image_name, image = extracted
        elif kwargs.pop('make', None):
            image_name = 'image.jpg'
            image = utils.django_image(image_name, **kwargs)
        else:
            return
        self.press_release_photo.save(image_name, image)
