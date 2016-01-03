import factory


def get_create_function(photo_model):
    class PhotoFactory(factory.DjangoModelFactory):
        class Meta:
            model = photo_model

        title = factory.Sequence(lambda n: 'title {}'.format(n))

        image = factory.django.ImageField(color='blue')

    def create_photos(obj, create, extracted, **kwargs):
        if extracted:
            obj.photos.add(extracted)
        number = int(kwargs.pop('n', 0))
        for _ in range(number):
            photo = PhotoFactory.create(content_object=obj, **kwargs)
            obj.photos.add(photo)

    return create_photos
