import factory

from ... import utils
from .models import MockPhoto, MockRelated


def get_create_function(photo_model):
    class PhotoFactory(factory.DjangoModelFactory):
        FACTORY_FOR = photo_model

        title = factory.Sequence(lambda n: 'title {}'.format(n))

        @factory.post_generation
        def image(self, create, extracted, **kwargs):
            if extracted:
                image_name, image = extracted
            else:
                image_name = 'image.jpg'
                image = utils.django_image(image_name, **kwargs)
            self.image.save(image_name, image)

    def create_photos(obj, create, extracted, **kwargs):
        if extracted:
            obj.photos.add(extracted)
        number = int(kwargs.pop('n', 0))
        for _ in range(number):
            photo = PhotoFactory.create(content_object=obj, **kwargs)
            obj.photos.add(photo)

    return create_photos


class MockRelatedFactory(factory.DjangoModelFactory):
    FACTORY_FOR = MockRelated


class MockPhotoFactory(factory.DjangoModelFactory):
    FACTORY_FOR = MockPhoto

    title = factory.Sequence(lambda n: 'title {}'.format(n))
    content_object = factory.SubFactory(MockRelatedFactory)

    @factory.post_generation
    def image(self, create, extracted, **kwargs):
        if extracted:
            image_name, image = extracted
        else:
            image_name = 'image.jpg'
            image = utils.django_image(image_name, **kwargs)
        self.image.save(image_name, image)
