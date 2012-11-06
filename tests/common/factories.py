import factory

from django.db.models import Max
from .functions import django_image


class DjangoFactory(factory.Factory):
    'Base factory to use next available id in sequence'
    ABSTRACT_FACTORY = True

    @classmethod
    def _setup_next_sequence(cls):
        return (cls._associated_class.objects.aggregate(Max('id')).values()[0] or 0) + 1


class BasePhotoFactory(DjangoFactory):
    ABSTRACT_FACTORY = True

    title = factory.Sequence(lambda n: 'Title{}'.format(n))
    caption = 'caption for this image'
    image = factory.Sequence(lambda n: django_image(n, 200))

    position = factory.Sequence(lambda n: n)
