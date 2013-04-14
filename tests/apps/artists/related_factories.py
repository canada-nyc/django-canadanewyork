def create_artists(self, create, extracted, **kwargs):
    from .factories import ArtistFactory
    if extracted:
        self.artists.add(extracted)
    number = int(kwargs.pop('n', 0))
    for _ in range(number):
        artist = ArtistFactory.create(**kwargs)
        self.artists.add(artist)


def create_artist(self, create, extracted, **kwargs):
    from .factories import ArtistFactory
    if extracted:
        self.artist = extracted
    elif kwargs.pop('make', None):
        self.artist = ArtistFactory.create(**kwargs)
    else:
        return None
    self.save()
