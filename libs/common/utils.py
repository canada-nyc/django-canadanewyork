import os
import imp


SITE_ROOT = os.path.dirname(imp.find_module('manage')[1])


def rel_path(relative_path):
    '''
    given any path relative to the `SITE_ROOT`, returns the full path
    '''
    return os.path.normpath(os.path.join(SITE_ROOT, relative_path))


def sentance_join(list):
    '''
    Returns the list joined properly to add to text.

    For example:

    first, second, and third
    first and second
    first
    '''
    if not len(list):
        return ''
    if len(list) == 1:
        return list[0]
    elif len(list) == 2:
        return ' and '.join(list)
    else:
        list[-1] = 'and ' + list[-1]
        return ', '.join(list)
