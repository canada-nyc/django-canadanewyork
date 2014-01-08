from distutils.util import strtobool
from invoke.exceptions import ParseError


def _resolve_app_label(ctx, app_label):
    '''
    Returns the app_label passed in, or the default if None is passed in.
    '''
    return app_label or ctx['default_app_label']


def _get_single_app(ctx, app_label):
    '''
    Returns the app from the Invoke context
    '''
    return ctx['apps'][app_label]


def confirm(ctx, prompt='Continue?', failure_prompt='User cancelled task'):
    '''
    Prompt the user to continue. Repeat on unknown response. Raise
    Failure Exception on negative response
    '''
    response = raw_input(prompt)

    try:
        response_bool = strtobool(response)
    except ValueError:
        print 'Unkown Response. Confirm with y, yes, t, true, on or 1; cancel with n, no, f, false, off or 0.'
        confirm(ctx, prompt, failure_prompt)

    if not response_bool:
        raise ParseError(failure_prompt)


def confirm_app(ctx, app, prompt):
    '''
    If the app has a ``confirm`` key set to ``True`` then prompt the user
    for confirmation before coninueing
    '''
    if app.pop('confirm', False):
        confirm(ctx, prompt=prompt)


def get_app(ctx, app_label):
    '''
    Get an app from the context, logs the label, and confirms in neccesary
    '''
    resolved_label = _resolve_app_label(ctx, app_label)
    app = _get_single_app(ctx, resolved_label)
    confirm_app(ctx, app, prompt='Really run on {}?'.format(app_label))
    return app


def get_apps(ctx, source_app_label, destination_app_label):
    '''
    Get two apps from the context, logs the labels, and confirms the destionation
    if neccesary
    '''
    source_resolved_label, destination_resolved_label = [_resolve_app_label(ctx, source_app_label), _resolve_app_label(ctx, destination_app_label)]
    source_app, destination_app = [_get_single_app(ctx, source_resolved_label), _get_single_app(ctx, destination_resolved_label)]

    confirm_app(ctx, destination_app, prompt='Really run on {}?'.format(destination_app_label))

    if source_app == destination_app:
        raise ParseError('Source and destination apps are the same')

    return source_app, destination_app
