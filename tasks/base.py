from distutils.util import strtobool
from invoke.exceptions import ParseError

from .utils import confirm


def _resolve_app_label(ctx, app_label):
    '''
    Returns the app_label passed in, or the default if None is passed in.
    '''
    return app_label or ctx['default_app_label']


def _get_single_app(ctx, app_label):
    '''
    Returns the app from the Invoke context
    '''
    try:
        return ctx['apps'][app_label]
    except KeyError:
        raise ParseError('"{}" not valid app label. Choices are: {}'.format(
            app_label,
            ' '.join(ctx['apps'].keys())
        ))


def get_app(ctx, app_label, prompt_confirm=True):
    '''
    Get an app from the context, logs the label, and confirms in neccesary
    '''
    resolved_label = _resolve_app_label(ctx, app_label)
    print '-> {}'.format(resolved_label)
    app = _get_single_app(ctx, resolved_label)
    if prompt_confirm and app.pop('confirm', False):
        confirm(prompt='Really run on {}?\n'.format(app_label))
    return app


def get_apps(ctx, source_app_label, destination_app_label):
    '''
    Get two apps from the context, logs the labels, and confirms the destionation
    if neccesary
    '''
    source_resolved_label, destination_resolved_label = [_resolve_app_label(ctx, source_app_label), _resolve_app_label(ctx, destination_app_label)]
    print '{} -> {}'.format(source_resolved_label, destination_resolved_label)
    source_app, destination_app = [_get_single_app(ctx, source_resolved_label), _get_single_app(ctx, destination_resolved_label)]

    if confirm and destination_app.pop('confirm', False):
        confirm(prompt='Really run on {}?\n'.format(destination_resolved_label))

    if source_app == destination_app:
        raise ParseError('Source and destination apps are the same')

    return source_app, destination_app
