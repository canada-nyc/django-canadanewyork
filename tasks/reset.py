from invoke import ctask as task

from .base import get_app
from .apps import manage


@task()
def database(ctx, app_label=None, test_data=False):
    print 'Resetting Database'
    app = get_app(ctx, app_label)

    if app['type'] == 'local':
        database_name = manage(ctx, 'database_name', app_label, hide='out').stdout
        ctx.run('dropdb ' + database_name)
        ctx.run('createdb ' + database_name)
    elif app['type'] == 'heroku':
        ctx.run('heroku pg:reset DATABASE_URL -a {0} --confirm {0}'.format(
            app['name']
        ))

    manage(ctx, 'init_db', app_label)

    if test_data:
        manage(ctx, 'test_data', app_label)


@task()
def cache(ctx, app_label):
    print 'Resetting Cache'
    manage(ctx, 'clear_cache', app_label)


@task()
def storage(ctx, app_label, only_static=False):
    print 'Resetting Storage'
    if only_static:
        manage(ctx, 'wipe_storage --only_static', app_label)
    else:
        manage(ctx, 'wipe_storage', app_label)
    manage(ctx, 'collectstatic --verbosity=0 --noinput', app_label)
