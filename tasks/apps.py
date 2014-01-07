from invoke import ctask as task

from .base import get_app


@task
def manage(ctx, command='', app_label=None, *args, **kwargs):
    app = get_app(ctx, app_label)

    if app['type'] == 'local':
        shell_command = 'foreman run python manage.py {}'.format(command)
    elif app['type'] == 'heroku':
        shell_command = "heroku run 'python manage.py {}' -a {}".format(
            command,
            app['name']
        )
    return ctx.run(shell_command, *args, **kwargs)


@task
def get_env_variable(ctx, key, app_label=None):
    app = get_app(ctx, app_label)

    if app['type'] == 'local':
        shell_command = 'echo $' + key
    elif app['type'] == 'heroku':
        shell_command = "heroku config:get {} -a {}".format(
            key,
            app['name']
        )
    return ctx.run(shell_command, hide='stdout').stdout
