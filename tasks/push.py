from invoke import Collection, ctask as task
from invoke.exceptions import ParseError

from .base import get_app, get_apps
from .apps import manage
from .reset import cache as reset_cache, storage as reset_storage


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
def env(ctx, app_label):
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
def code(ctx, source_label='dev', destination_label='prod'):
    '''
    Pushes code between heroku apps using the pipeline heroku command
    '''
    print 'Pushing code'
    source, destination = get_apps(ctx, source_label, destination_label)

    ctx.run('heroku pipeline:promote --app {}'.format(source['name']))


@task
def all(ctx, source_label='dev', destination_label='prod', syncdb=True, static=True, wipe_static=False, wipe_cache=True):
    '''
    Pushes code between heroku apps, and optionally syncs the database and
    static of the destination app with the newly pushed code. Also can wipe
    the cache of the destination app and static.
    '''
    print 'Pushing all'
    code(ctx, source_label, destination_label)

    if syncdb:
        manage(ctx, 'syncdb --migrate', destination_label)
    if wipe_cache:
        reset_cache(ctx, destination_label)
    if wipe_static:
        reset_storage(ctx, destination_label, only_static=True)
    elif static:
        manage(ctx, 'collectstatic --verbosity=0 --noinput', destination_label)


namespace = Collection(env, code, all)
