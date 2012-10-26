import factory

from .models import SlugifyModel, RelatedModel
from ...common.factories import DjangoFactory


class RelatedModelFactory(DjangoFactory):
    FACTORY_FOR = RelatedModel

    text = factory.Sequence(lambda n: 'text{}'.format(n))


class SlugModelFactory(DjangoFactory):
    FACTORY_FOR = SlugifyModel

    text = factory.Sequence(lambda n: 'text{}'.format(n))
    text2 = factory.Sequence(lambda n: 'text2{}'.format(n))
    related_model = factory.LazyAttribute(lambda a: RelatedModelFactory())
