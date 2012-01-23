import os


def cap(self, *args):
    """capatilize x model fields"""
    for field in args:
        value = getattr(self, field)
        setattr(self, field, value.title())

def rel_path(ending):
    """ouput the absolute path to a relative file name"""
    return os.path.abspath(os.path.join(os.path.dirname(__file__), str(ending)))
