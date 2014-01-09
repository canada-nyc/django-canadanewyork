from invoke import Collection, ctask as task

ns = Collection()
from .base import get_apps
from .apps import manage, get_env_variable
from .reset import _wipe_database, _set_site


@task()
def database(ctx, source_label=None, destination_label=None):
    '''
    Wipes the destination database and then copies the source database to it,
    finally setting the Site object to the correct host.
    '''
    print 'Cloning Database'
    source, destination = get_apps(ctx, source_label, destination_label)

    _wipe_database(ctx, destination_label)

    if 'local' in [source['type'], destination['type']]:
        local_database_name = ctx.run(
            'foreman run python manage.py database_name',
            hide='out'
        ).stdout
        if source['type'] == 'local':
            pg_command = 'push'
            heroku_app_name = destination['name']
            source_db, dest_db = (local_database_name, 'DATABASE_URL')
        else:
            pg_command = 'pull'
            heroku_app_name = source['name']
            source_db, dest_db = ('DATABASE_URL', local_database_name)

        ctx.run(
            'heroku pg:{} {} {} -a {}'.format(
                pg_command,
                source_db,
                dest_db,
                heroku_app_name
            )
        )
    else:
        ctx.run(
            'heroku pgbackups:capture '
            '-a {} --expire'.format(source['name'])
        )

        source_url = ctx.run(
            'heroku pgbackups:url -a {}'.format(source['name']),
            hide='out'
        ).stdout

        ctx.run("heroku pgbackups:restore DATABASE_URL '{}' -a {} --confirm {}".format(
            source_url,
            destination['name'],
            destination['name'],
        ))

    _set_site(ctx, destination_label)


@task()
def storage(ctx, source_label=None, destination_label=None):
    '''
    Clones the S3 bucket from the source to the destination, running the
    clone command on the source. Only works when both use S3 storage.
    '''
    print 'Cloning Storage'
    get_apps(ctx, source_label, destination_label)

    bucket_names = map(
        lambda app_label: get_env_variable(ctx, 'AWS_BUCKET', app_label),
        [source_label, destination_label]
    )

    manage(ctx, 'clone_bucket {} {}'.format(*bucket_names), source_label)


# @task()
# def code(ctx, source_label=None, destination_label=None):
#     apps = AppManager(ctx)(source_label, destination_label)
#     source_apps_pipeline =
#     if getattr(apps.source, 'pipeline', destination_label)
#     apps.source.pipeline
#     bucket_names = map(
#         lambda app: get_env_variable(ctx, app, 'AWS_BUCKET'),
#         (apps.source, apps.destination)
#     )

#     manage(ctx, source_label, 'clone_bucket {} {}'.format(*bucket_names))

@task()
def all(ctx, source_label=None, destination_label=None):
    '''
    Clones database and storage from source to destination.
    '''
    print 'Cloning All'
    database(ctx, source_label, destination_label)
    storage(ctx, source_label, destination_label)

ns = Collection(all, database, storage)
