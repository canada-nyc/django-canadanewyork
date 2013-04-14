import factory

from apps.photos.models import Photo

from ... import utils


class PhotoFactory(factory.DjangoModelFactory):
    FACTORY_FOR = Photo

    @factory.post_generation
    def image(self, create, extracted, **kwargs):
        if extracted:
            image_name, image = extracted
        else:
            image_name = 'image.jpg'
            image = utils.django_image(image_name, **kwargs)
        self.image.save(image_name, image)
