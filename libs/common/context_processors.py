import os


def sentry_dsn(request):
    return {'SENTRY_DSN': os.environ['SENTRY_DSN']}
