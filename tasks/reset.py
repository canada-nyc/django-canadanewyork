from invoke import ctask as task

from .base import AppManager
from .apps import manage


@task()
def database(ctx, app_label=None, test_data=False):
    app = AppManager(ctx)(app_label)

    if app.type == 'local':
        database_name = manage(ctx, app_label, 'database_name', hide='out').stdout
        ctx.run('dropdb ' + database_name)
        ctx.run('createdb ' + database_name)
    elif app.type == 'heroku':
        ctx.run('heroku pg:reset DATABASE_URL -a {0} --confirm {0}'.format(
            app.name
        ))

    manage(ctx, app_label, 'init_db')

    if test_data:
        manage(ctx, app_label, 'test_data')


@task()
def cache(ctx, app_label=None):
    manage(ctx, app_label, 'clear_cache')


@task()
def storage(ctx, app_label=None, only_static=False):
    if only_static:
        manage(ctx, app_label, 'wipe_storage --only_static')
    else:
        manage(ctx, app_label, 'wipe_storage')
    manage(ctx, app_label, 'collectstatic --verbosity=0 --noinput')
