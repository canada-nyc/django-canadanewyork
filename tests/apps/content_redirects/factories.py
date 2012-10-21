import factory

from .models import RedirectModel, RedirectModel_2
from ...common.factories import DjangoFactory


class RedirectModelFactory(DjangoFactory):
    FACTORY_FOR = RedirectModel

    text = factory.Sequence(lambda n: 'text{}'.format(n))
    old_path = factory.Sequence(lambda n: 'path/{}'.format(n))


class RedirectModel_2Factory(DjangoFactory):
    FACTORY_FOR = RedirectModel_2

    text = factory.Sequence(lambda n: 'text{}'.format(n))
    old_path = factory.Sequence(lambda n: 'path_2/{}'.format(n))
