from invoke import ctask as task

from .base import get_apps
from .apps import manage, get_env_variable
from .reset import database as reset_database


@task()
def database(ctx, source_label=None, destination_label=None):
    source, destination = get_apps(ctx, source_label, destination_label)

    reset_database(ctx, destination_label)

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

        ctx.run('# Creating backup of target app. To revert run:', echo=True)
        ctx.run(
            '# heroku pgbackups:restore DATABASE_URL -a {}'.format(
                destination['name']
            ),
            echo=True
        )
        ctx.run(
            'heroku pgbackups:capture '
            '-a {} --expire'.format(destination['name'])
        )

        source_url = ctx.run(
            'heroku pgbackups:url -a {}'.format(source['name']),
            hide='out'
        ).stdout

        ctx.run('heroku pgbackups:restore DATABASE_URL {} -a {}'.format(
            source_url,
            destination['name'],
        ))


@task()
def storage(ctx, source_label=None, destination_label=None):
    print 'Cloning Storage'
    get_apps(ctx, source_label, destination_label)

    bucket_names = map(
        lambda app: get_env_variable(ctx, app, 'AWS_BUCKET'),
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
