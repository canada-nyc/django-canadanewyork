from invoke import ctask as task

from .base import get_app


@task
def manage(ctx, command='', app_label=None, **kwargs):
    '''
    Runs a manage.py command, through foreman locally or heroku run remotely.

    Mostly for internal use, returns the running command, in case you want to
    get stdout
    '''
    print 'Running "{}" management command'.format(command)
    app = get_app(ctx, app_label)

    if app['type'] == 'local':
        shell_command = 'foreman run python manage.py {}'.format(command)
    elif app['type'] == 'heroku':
        shell_command = "heroku run 'python manage.py {}' -a {}".format(
            command,
            app['name']
        )
    kwargs.setdefault('pty', True)
    return ctx.run(shell_command, **kwargs)


@task
def get_env_variable(ctx, key, app_label=None):
    '''
    Gets a variable from the environment, through foreman locally or heroku
    config remotely.

    Mostly for internal use, returns the value of the variable
    '''
    print 'Getting "{}" from environemnt'.format(key)
    app = get_app(ctx, app_label, prompt_confirm=False)

    if app['type'] == 'local':
        shell_command = 'foreman run printenv ' + key
    elif app['type'] == 'heroku':
        shell_command = "heroku config:get {} -a {}".format(
            key,
            app['name']
        )
    value = ctx.run(shell_command, hide='stdout').stdout.strip()
    print value
    return value
