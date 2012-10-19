import factory

from .models import
from ...common.factories import DjangoFactory


class ContentRedirectModelFactory(DjangoFactory):
    FACTORY_FOR = ContentRedirectModel

    text = factory.Sequence(lambda n: 'text{}'.format(n))
    old_path = factory.Sequence(lambda n: 'path/{}'.format(n))


class ContentRedirectModel_2Factory(DjangoFactory):
    FACTORY_FOR = ContentRedirectModel_2

    text = factory.Sequence(lambda n: 'text{}'.format(n))
    old_path = factory.Sequence(lambda n: 'path_2/{}'.format(n))
