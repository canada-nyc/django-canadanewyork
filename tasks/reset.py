from invoke import Collection, ctask as task

from .base import get_app
from .apps import manage, start_if_local


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
        # have to stop web as well, so it is relinked
        ctx.run('docker-compose stop db web')
        ctx.run('docker-compose rm --force db')
        if not recreate_local:
            print 'Removing auto-created local database'
            ctx.run("docker-compose run db bash -c 'dropdb postgres --host=$DB_1_PORT_5432_TCP_ADDR --user=postgres'")
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
    database(ctx, app_label, test_data)
    cache(ctx, app_label)
    storage(ctx, app_label)


namespace = Collection(database, cache, storage, all, images)
