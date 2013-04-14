def create_press(self, create, extracted, **kwargs):
    from .factories import PressFactory
    if extracted:
        self.press.add(extracted)
    number = int(kwargs.pop('n', 0))
    for _ in range(number):
        press = PressFactory.create(**kwargs)
        self.press.add(press)
