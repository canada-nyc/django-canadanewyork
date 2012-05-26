import os


def cap(self, *args):
    """capatilize x model fields"""
    for field in args:
        value = getattr(self, field)
        setattr(self, field, value.title())


def rel_path(ending):
    """output the absolute path to a relative file name"""
    return os.path.join(os.path.dirname(__file__), str(ending))


def add_to_middleware(MIDDLEWARE_CLASSES_old, middleware, prepend=False):
    if middleware not in MIDDLEWARE_CLASSES_old:
        if prepend:
            return (middleware,) + MIDDLEWARE_CLASSES_old
        else:
            return MIDDLEWARE_CLASSES_old + (middleware,)
    else:
        return MIDDLEWARE_CLASSES_old
