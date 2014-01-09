from invoke import Collection, ctask as task
from invoke.exceptions import ParseError

from .base import get_app
from .apps import manage, get_env_variable
from .reset import _wipe_database, _set_site


def _get_env_var_paths(ctx, app):
    '''
    Returns a iterable of all the paths for environmental variabial files
    for that app
    '''
    for path in ctx['base_env_files']:
        yield path
    if 'env_file' in app:
        yield app['env_file']


@task(aliases=['env'])
def environemntal_variables(ctx, app_label):
    '''
    Pushes environemntal variables from the local configs/env/* files to
    Heroku apps.
    '''
    print 'Pushing environmental variable'
    app = get_app(ctx, app_label)
    if not app['type'] == 'heroku':
        raise ParseError('Can only push environmental variables to Heroku apps')

    for path in _get_env_var_paths(ctx, app_label):
        ctx.run('heroku config:push -o "{}"'.format(path))


namespace = Collection(environemntal_variables)
