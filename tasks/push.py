from invoke import Collection, ctask as task
from invoke.exceptions import ParseError

from .base import get_app
from .apps import manage
from .reset import cache as reset_cache, storage as reset_storage
from .clone import code as clone_code


def _get_env_var_paths(ctx, app):
    '''
    Returns a iterable of all the paths for environmental variabial files
    for that app
    '''
    for path in ctx['base_env_files']:
        yield path
    if 'env_file' in app:
        yield app['env_file']


@task(aliases=['environemntal_variables'])
def env(ctx, app_label=None):
    '''
    Pushes environemntal variables from the local configs/env/* files to
    Heroku apps.
    '''
    print 'Pushing environmental variables'
    app = get_app(ctx, app_label)
    if not app['type'] == 'heroku':
        raise ParseError('Can only push environmental variables to Heroku apps')

    for path in _get_env_var_paths(ctx, app):
        ctx.run('heroku config:push -o "{}" --app {}'.format(path, app['name']))


@task
def all(ctx, syncdb=True, static=True, wipe_static=False, wipe_cache=True):
    '''
    Pushes code between heroku apps, and optionally syncs the database and
    static of the destination app with the newly pushed code. Also can wipe
    the cache of the destination app and static.
    '''
    print 'Pushing all'
    source_label, destination_label = (ctx['staging_app_label'], ctx['production_app_label'])

    clone_code(ctx, source_label, destination_label)

    if syncdb:
        manage(ctx, 'syncdb --migrate', destination_label)
    if wipe_cache:
        reset_cache(ctx, destination_label)
    if wipe_static:
        reset_storage(ctx, destination_label, only_static=True)
    elif static:
        manage(ctx, 'collectstatic --verbosity=0 --noinput', destination_label)


namespace = Collection(env, all)