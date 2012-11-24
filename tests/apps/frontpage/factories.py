import factory

from apps.frontpage.models import Frontpage
from ...common.factories import DjangoFactory
from ..exhibitions.factories import ExhibitionFactory


class FrontpageFactory(DjangoFactory):
    FACTORY_FOR = Frontpage

    exhibition = factory.LazyAttribute(lambda a: ExhibitionFactory(photos__n=1))
    exhibition_image = factory.LazyAttribute(lambda a: a.exhibition.photos.all()[0])
