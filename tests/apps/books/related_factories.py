def create_books(self, create, extracted, **kwargs):
    from .factories import BookFactory
    if extracted:
        self.books.add(extracted)
    number = int(kwargs.pop('n', 0))
    for _ in range(number):
        press = BookFactory.create(**kwargs)
        self.books.add(press)
