from invoke import ctask as task

from .base import AppManager


@task
def manage(ctx, app_label, command, *args, **kwargs):
    app = AppManager(ctx)(app_label)
    if app.type == 'local':
        shell_command = 'foreman run python manage.py {}'.format(command)
    elif app.type == 'heroku':
        shell_command = "heroku run 'python manage.py {}' -a {}".format(
            command,
            app.name
        )
    return ctx.run(shell_command, *args, **kwargs)


@task
def get_env_variable(ctx, app_label, key):
    app = AppManager(ctx)(app_label)
    if app.type == 'local':
        shell_command = 'echo $' + key
    elif app.type == 'heroku':
        shell_command = "heroku config:get {} -a {}".format(
            key,
            app.name
        )
    return ctx.run(shell_command, hide='stdout').stdout
