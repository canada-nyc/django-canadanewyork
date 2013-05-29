import factory

from .models import RelatedPhotoModel
from tests.apps.photos.related_factories import create_photos


class RelatedPhotoFactory(factory.DjangoModelFactory):
    FACTORY_FOR = RelatedPhotoModel

    photos = factory.PostGeneration(create_photos)
