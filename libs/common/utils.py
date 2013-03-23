import os
import imp

from honcho import command


SITE_ROOT = os.path.dirname(imp.find_module('manage')[1])


def rel_path(relative_path):
    '''
    given any path relative to the `SITE_ROOT`, returns the full path
    '''
    return os.path.normpath(os.path.join(SITE_ROOT, relative_path))


def export_env_files(*file_paths):
    content = []
    H = command.Honcho()
    for envfile in file_paths:
        with open(rel_path(envfile)) as f:
            content.append(f.read())
    env = H.parse_env('\n'.join(content))
    H.set_env(env)
