import factory

from ... import utils


def PhotoFactory(photo_model):
    class PhotoFactory(factory.DjangoModelFactory):
        class Meta:
            model = photo_model

        title = utils.FakerTitle()
        image = utils.FakerImageField()

        position = factory.Sequence(lambda n: n)

    return PhotoFactory


def get_create_function(photo_model):
    def create_photos(obj, create, extracted, **kwargs):
        if extracted:
            obj.photos.add(extracted)
        number = int(kwargs.pop('n', 0))
        for _ in range(number):
            photo = PhotoFactory(photo_model).create(content_object=obj, **kwargs)
            obj.photos.add(photo)

    return create_photos
