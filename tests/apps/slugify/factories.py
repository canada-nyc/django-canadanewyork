import factory

from .models import SlugifyModel, RelatedModel, SlugifyDateModel
from ...common.factories import DjangoFactory


class RelatedModelFactory(DjangoFactory):
    FACTORY_FOR = RelatedModel

    text = factory.Sequence(lambda n: 'text{}'.format(n))


class SlugifyModelFactory(DjangoFactory):
    FACTORY_FOR = SlugifyModel

    text = factory.Sequence(lambda n: 'text{}'.format(n))
    related_model = factory.LazyAttribute(lambda a: RelatedModelFactory())


class SlugifyDateModelFactory(DjangoFactory):
    FACTORY_FOR = SlugifyDateModel

    text = factory.Sequence(lambda n: 'text{}'.format(n))
