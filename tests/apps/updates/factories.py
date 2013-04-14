import factory

from apps.updates.models import Update
from ..photos.related_factories import create_photos


class UpdateFactory(factory.DjangoModelFactory):
    FACTORY_FOR = Update

    photos = factory.PostGeneration(create_photos)
