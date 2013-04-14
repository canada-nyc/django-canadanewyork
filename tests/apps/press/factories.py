import datetime

import factory

from apps.press.models import Press
from ..artists.related_factories import create_artist
from ..exhibitions.related_factories import create_exhibition


class PressFactory(factory.DjangoModelFactory):

    FACTORY_FOR = Press

    date = datetime.date.today()

    exhibition = factory.PostGeneration(create_exhibition)
    artist = factory.PostGeneration(create_artist)
