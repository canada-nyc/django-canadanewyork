def cap(self, *args):
    for field in args:
        value = getattr(self, field)
        setattr(self, field, value.title())
