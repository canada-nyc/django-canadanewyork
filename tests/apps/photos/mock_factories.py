import factory
from .models import MockRelated, MockPhoto


class MockRelatedFactory(factory.DjangoModelFactory):

    class Meta:
        model = MockRelated


class MockPhotoFactory(factory.DjangoModelFactory):

    class Meta:
        model = MockPhoto

    title = factory.Sequence(lambda n: 'title {}'.format(n))
    content_object = factory.SubFactory(MockRelatedFactory)

    image = factory.django.ImageField(color='blue')
