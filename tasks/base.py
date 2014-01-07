def get_app(ctx, app_label):
    '''
    Returns either the app from the Invoke context from the label passed in,
    or if passed in None, then return the default app
    '''
    default_app_label = ctx['default_app_label']
    return ctx['apps'][app_label or default_app_label]
