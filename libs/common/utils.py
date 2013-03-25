import os
import imp


SITE_ROOT = os.path.dirname(imp.find_module('manage')[1])


def rel_path(relative_path):
    '''
    given any path relative to the `SITE_ROOT`, returns the full path
    '''
    return os.path.normpath(os.path.join(SITE_ROOT, relative_path))
