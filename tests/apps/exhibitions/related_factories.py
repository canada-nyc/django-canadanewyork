def create_exhibitions(self, create, extracted, **kwargs):
    from .factories import ExhibitionFactory
    if extracted:
        self.exhibitions.add(create)
    number = int(kwargs.pop('n', 0))
    for _ in range(number):
        exhibition = ExhibitionFactory.create(**kwargs)
        self.exhibitions.add(exhibition)


def create_exhibition(self, create, extracted, **kwargs):
    from .factories import ExhibitionFactory
    if extracted:
        self.exhibition = extracted
    elif kwargs.pop('make', None):
        self.exhibition = ExhibitionFactory.create(**kwargs)
    else:
        return
    self.save()
