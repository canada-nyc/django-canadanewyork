import os


def cap(self, *args):
    """capatilize x model fields"""
    for field in args:
        value = getattr(self, field)
        setattr(self, field, value.title())


def rel_path(ending='/'):
    """output the absolute path of an ending joined to the current file path"""
    return os.path.join(os.path.dirname(__file__), str(ending))


def add_to_middleware(MIDDLEWARE_CLASSES, middleware, prepend=False):
    if middleware not in MIDDLEWARE_CLASSES:
        if prepend:
            return (middleware,) + MIDDLEWARE_CLASSES
        else:
            return MIDDLEWARE_CLASSES + (middleware,)
    else:
        return MIDDLEWARE_CLASSES
