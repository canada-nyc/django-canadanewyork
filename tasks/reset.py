from invoke import Collection, ctask as task

from .base import get_app
from .apps import manage


@task()
def _wipe_database(ctx, app_label=None):
    '''
    Only wipes database, does not create new one.
    '''
    print 'Wiping Database'
    app = get_app(ctx, app_label)

    if app['type'] == 'local':
        database_name = manage(ctx, 'database_name', app_label, hide='out').stdout
        ctx.run('dropdb ' + database_name)
    elif app['type'] == 'heroku':
        ctx.run('heroku pg:reset DATABASE_URL -a {0} --confirm {0}'.format(
            app['name']
        ))


@task()
def database(ctx, app_label=None, test_data=False):
    '''
    Wipes the database, then initializes it using ``manage.py init_db`` and
    optionally adds some test data from ``manage.py test_data``.
    '''
    if test_data:
        print 'Resetting Database and adding test data'
    else:
        print 'Resetting Database'
    _wipe_database(ctx, app_label)
    manage(ctx, 'init_db', app_label)

    if test_data:
        manage(ctx, 'test_data', app_label)


@task()
def cache(ctx, app_label):
    '''
    Deletes the default cache
    '''
    print 'Resetting Cache'
    manage(ctx, 'clear_cache', app_label)


@task()
def storage(ctx, app_label, only_static=False):
    '''
    Deletes every item in the storage, either locally or on S3. It can also
    only delete the ``canada`` static folder, in order to help on invalidating
    cached static files.
    '''
    if only_static:
        print 'Resetting only static. Only works on S3, not local files'
    else:
        print 'Resetting Storage'
    if only_static:
        manage(ctx, 'delete_canada_static', app_label)
    else:
        manage(ctx, 'wipe_storage', app_label)
    manage(ctx, 'collectstatic --verbosity=0 --noinput', app_label)


@task()
def all(ctx, app_label, test_data=False, only_static=False):
    '''
    Resets The database, cache, and storage.
    '''
    print 'Resetting All'
    database(ctx, app_label, test_data)
    cache(ctx, app_label)
    storage(ctx, app_label, only_static)


namespace = Collection(database, cache, storage, all)
