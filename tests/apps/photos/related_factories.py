def create_photos(self, create, extracted, **kwargs):
    from .factories import PhotoFactory
    if extracted:
        self.photos.add(extracted)
    number = int(kwargs.pop('n', 0))
    for _ in range(number):
        photo = PhotoFactory.create(**kwargs)
        self.photos.add(photo)
