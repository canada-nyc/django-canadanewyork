import factory

from apps.updates.models import Update, UpdatePhoto
from ..photos.factories import get_create_function
from ... import utils


class UpdateFactory(factory.DjangoModelFactory):
    FACTORY_FOR = Update

    photos = factory.PostGeneration(get_create_function(UpdatePhoto))
    post_date = utils.FuzzyDate()
