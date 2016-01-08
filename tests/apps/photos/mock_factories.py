import factory
from .models import MockRelated, MockPhoto

from .factories import PhotoFactory


class MockRelatedFactory(factory.DjangoModelFactory):

    class Meta:
        model = MockRelated


class MockPhotoFactory(PhotoFactory(MockPhoto)):
    content_object = factory.SubFactory(MockRelatedFactory)
