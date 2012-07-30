import factory

from canada.apps.frontpage.models import Frontpage


class FrontpageFactory(factory.Factory):
    FACTORY_FOR = Frontpage

    custom_title = factory.LazyAttributeSequence(lambda _, n: 'Custom Title {}'.format(n))
    activated = True
