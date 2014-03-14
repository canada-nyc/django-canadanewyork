from invoke import Collection, ctask as task, exceptions

from .base import get_app
from .apps import manage


@task()
def _wipe_database(ctx, app_label=None, recreate_local=True):
    '''
    Wipes the database. By default will create a new database using the
    database_name management command to get the name from the settings.
    If you dont want to create a new one, call with ``recreate_local=False``
    '''
    print 'Wiping Database'
    app = get_app(ctx, app_label)

    if app['type'] == 'local':
        database_name = manage(
            ctx, 'database_name', app_label, hide='out').stdout
        # Don't fail if this comand exits because the database does not
        # existerror
        dropdb = ctx.run('dropdb ' + database_name, warn=True, hide='err', pty=True)
        database_does_not_exist = 'database "{}" does not exist'.format(
            database_name)
        failed_because_database_does_not_exist = database_does_not_exist in dropdb.stderr
        if not dropdb.ok and not failed_because_database_does_not_exist:
            raise exceptions.Failure(dropdb)

        if recreate_local:
            print 'Creating local database'
            ctx.run('createdb ' + database_name)
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
def storage(ctx, app_label):
    '''
    Deletes every item in the storage, either locally or on S3.
    '''
    print 'Resetting Storage'
    manage(ctx, 'wipe_storage', app_label)
    manage(ctx, 'collectstatic --noinput', app_label)


@task(aliases=['transformed_images'])
def images(ctx, app_label):
    '''
    Retransforms all the Photo subclasses
    '''
    manage(
        ctx,
        ('retransform '
         'artists.ArtistPhoto '
         'exhibitions.ExhibitionPhoto '
         'updates.UpdatePhoto'),
        app_label,
        pty=True
    )


@task()
def all(ctx, app_label, test_data=True):
    '''
    Resets The database, cache, and storage.
    '''
    print 'Resetting All'
    cache(ctx, app_label)
    storage(ctx, app_label)
    database(ctx, app_label, test_data)


namespace = Collection(database, cache, storage, all, images)
