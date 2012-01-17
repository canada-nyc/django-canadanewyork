def cap(self, *args):
    """capatilize x model fields"""
    for field in args:
        value = getattr(self, field)
        setattr(self, field, value.title())
